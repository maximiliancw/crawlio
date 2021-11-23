import asyncio
import random
import time
from collections import namedtuple
from typing import Dict, Any, Generator, Union, List
from urllib.parse import urlparse, urljoin

import aiohttp
from parsel import Selector as Parsel


Request = namedtuple('Request', 'url')
Response = namedtuple('Response', ('url', 'headers', 'html'))

UA = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
)


class Crawler(object):

    def __init__(self, url: str, selectors: Dict[str, str] = None):
        self._url = url
        self._selectors = selectors
        parsed = urlparse(self._url)
        self._base_url = f"{parsed.scheme}://{parsed.netloc}/"
        self._headers = {'User-Agent': random.choice(UA)}
        self._loop = asyncio.get_event_loop()
        self._queue = {url}
        self._data = []

    async def run(self) -> List[Dict[str, Any]]:
        """ Main entrypoint for running a spider """
        print('Crawler started')
        # Handle responses as they're yielded (using an asynchronous generator)
        async for response in self._crawl():
            async for obj in self._scrape(response):
                # response is a new request object
                if isinstance(obj, Request):
                    self._queue.add(obj.url)
                # response is a new page item
                else:
                    self._data.append(obj)
        return self._data

    async def _crawl(self) -> Generator[Response, None, None]:
        """ Handles the actual crawling process """

        # Store set of processed URLs
        blacklist = set()

        # Use single session for this crawl (slightly better performance)
        async with aiohttp.ClientSession(headers=self._headers) as session:
            while len(self._queue):
                url = self._queue.pop()
                # Skip previously seen URLs
                if url in blacklist: continue
                # Download from url
                response = await session.get(url)
                blacklist.add(url)
                yield Response(
                    url=url,
                    # response.headers is a custom class, so we convert it to a dictionary
                    headers={k: v for k, v in response.headers.items()},
                    html=await response.text()
                )
                # Download delay for load reduction on server-side
                # await asyncio.sleep(0.1)    # TODO: make this download delay configurable

    async def _scrape(self, response: Response) -> Generator[Union[Request, Dict[str, Any]], None, None]:
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
        data = dict()
        if self._selectors:
            for field, query in self._selectors.items():
                extracted = dom.xpath(query).getall()   # Extract from HTML
                data[field] = extracted[0] if len(extracted) == 1 else extracted    # Transform single-element lists

        yield dict(url=response.url, headers=response.headers, data=data)


if __name__ == '__main__':
    """ Run this file for quick & dirty testing """
    fields = {
        'title': '/html/head/title/text()',
        # ...
    }
    crawler = Crawler('https://quotes.toscrape.com/', selectors=fields)
    start_time = time.time()
    results = asyncio.run(crawler.run(), debug=True)
    end_time = time.time()
    for item in results:
        print(item)

    duration = round(end_time - start_time, 2)
    print(f'Duration: {duration}s | Pages: {len(results)} | {round(len(results)/duration, 2)} p/s')
