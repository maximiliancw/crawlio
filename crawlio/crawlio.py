import asyncio
import random
import time
from dataclasses import dataclass
from typing import Dict, Any, Generator, Union, List, Callable
from urllib.parse import urlparse, urljoin

import aiohttp
from tqdm.asyncio import tqdm
from parsel import Selector as Parser


def identity(obj: List[Any]) -> Any:
    """ Return the identity of a list object """
    return obj


@dataclass
class Request:
    url: str


@dataclass
class Response:
    url: str
    status: int
    html: str


@dataclass
class Selector:
    name: str
    query: str
    type: str = 'xpath'
    process: Callable[[List[Any]], Any] = identity


class Crawler(object):
    user_agents = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    )

    def __init__(self, url: str, selectors: List[Selector] = None, delay: float = .2, timeout: float = 10.0):
        self._selectors = selectors
        parsed = urlparse(url)
        self._base_url = f"{parsed.scheme}://{parsed.netloc}/"
        self._headers = {'User-Agent': random.choice(self.user_agents)}
        self._delay = delay
        self._timeout = aiohttp.ClientTimeout(timeout)
        self._queue = {url}
        self.errors = dict()

    async def run(self) -> Dict[str, Any]:
        results = []
        start_time = time.time()

        async for response in tqdm(self._crawl(), desc='Crawling', ascii=False, unit=' pages'):
            async for obj in self._scrape(response):
                if isinstance(obj, Request):
                    self._queue.add(obj.url)
                else:
                    results.append(obj)

        duration = round(time.time() - start_time, 2)
        performance = round(len(results)/duration, 2)
        info = dict(pages=len(results), duration=duration, pps=performance, errors=self.errors)
        return dict(info=info, data=results)

    async def _crawl(self) -> Generator[Response, None, None]:
        seen_urls = set()
        async with aiohttp.ClientSession(headers=self._headers, timeout=self._timeout) as session:
            while len(self._queue):
                url = self._queue.pop()
                if url in seen_urls: continue   # Ignore previously seen URLs
                delay = random.uniform(.1, max(self._delay, .2))
                await asyncio.sleep(delay)   # Apply download delay
                try:
                    async with session.get(url) as response:
                        seen_urls.add(url)  # Mark URL as processed
                        yield Response(url=url, status=response.status, html=await response.text())
                except Exception as e:
                    self.errors[url] = str(e)

    async def _scrape(self, response: Response) -> Generator[Union[Request, Dict[str, Any]], None, None]:
        doc = Parser(text=response.html, type='html')
        # Scrape & filter links for crawling
        for link in doc.xpath('//a/@href').getall():
            # Handle relative links
            if link.startswith('/'):
                link = urljoin(self._base_url, link)
            # Follow links
            if self.follow(link):
                yield Request(link)

        # Scrape user-defined data
        data = dict()
        if self._selectors:
            for selector in self._selectors:
                if selector.type == 'xpath':
                    selection = doc.xpath(selector.query).getall()
                elif selector.type == 'css':
                    selection = doc.css(selector.query).getall()
                else:
                    raise ValueError(f"'{selector.type}' is not a valid selector type; use 'xpath' or 'css' instead")
                data[selector.name] = selector.process(selection)
        yield dict(url=response.url, status=response.status, **data)

    def follow(self, link: str) -> bool:
        """
        Determines whether the given link should be followed or ignored.
        You can overwrite this method to implement custom link filters
        """
        return link.startswith(self._base_url)  # Discard external links


if __name__ == '__main__':
    bot = Crawler(
        url='https://quotes.toscrape.com/',
        selectors=[
            Selector('links', '//a/@href'),
            Selector('heading', type='xpath', query='//h3//text()', process=lambda items: ' '.join(items))
        ]
    )
    output = asyncio.run(bot.run())
    for item in output["data"]:
        print(item)
