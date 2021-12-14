import asyncio
import random
import time
from collections import namedtuple
from typing import Dict, Any, Generator, Union, List
from urllib.parse import urlparse, urljoin

import aiohttp
from parsel import Selector as Parsel


Settings = namedtuple('Settings', ('max_concurrency', 'download_delay'))
Request = namedtuple('Request', 'url')
Response = namedtuple('Response', ('url', 'status', 'headers', 'html'))
Page = namedtuple('Page', ('url', 'meta', 'data'))

UA = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
)


class Crawler(object):

    def __init__(self, url: str, selectors: Dict[str, str] = None, delay: float = .3):
        self._url = url
        self._selectors = selectors
        parsed = urlparse(self._url)
        self._base_url = f"{parsed.scheme}://{parsed.netloc}/"
        self._headers = {'User-Agent': random.choice(UA)}
        self._loop = asyncio.get_event_loop()
        self._delay = delay
        self._queue = {url}
        self._data = []

    async def run(self) -> Dict[str, Any]:
        start_time = time.time()
        async for response in self._crawl():
            async for obj in self._scrape(response):
                # response is a new Request
                if isinstance(obj, Request):
                    self._queue.add(obj.url)
                # response is a new Page
                elif isinstance(obj, Page):
                    self._data.append(obj)
                else:
                    raise TypeError(f"{type(obj)} != {Page} or {Request}")
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        return dict(
            meta=dict(
                pages=len(self._data),
                duration=duration,
                performance=round(len(self._data)/duration, 2)
            ),
            data=self._data
        )

    async def _crawl(self) -> Generator[Response, None, None]:
        seen_urls = set()
        async with aiohttp.ClientSession(headers=self._headers) as session:
            while len(self._queue):
                url = self._queue.pop()
                if url in seen_urls: continue
                await asyncio.sleep(random.uniform(.01, max(self._delay, 0)))
                async with session.get(url) as response:
                    seen_urls.add(url)
                    yield Response(
                        url=url,
                        status=response.status,
                        headers={k: v for k, v in response.headers.items()},
                        html=await response.text()
                    )

    async def _scrape(self, response: Response) -> Generator[Union[Request, Page], None, None]:
        dom = Parsel(text=response.html)
        # Scrape (internal) links for crawling
        links = dom.xpath('//a/@href').getall()
        for link in links:
            # Prepend base_url to relative links
            if link.startswith('/'):
                link = urljoin(self._base_url, link)
            # Discard external links
            if not link.startswith(self._base_url):
                continue
            # Enqueue new request
            yield Request(link)

        # Scrape user-defined data
        data = {
            name: dom.xpath(query).getall()
            for name, query in self._selectors.items()
        } if self._selectors else None

        # Return scraped page
        metadata = dict(status=response.status, headers=response.headers)
        yield Page(url=response.url, meta=metadata, data=data)


if __name__ == '__main__':
    """ Run this file for quick & dirty testing """
    fields = {
        'title': '//title/text()'
    }
    crawler = Crawler('https://innovinati.com/', selectors=fields)
    results = asyncio.run(crawler.run(), debug=True)
    print(results["meta"])
    for item in results["data"]:
        print(item)
