<img width="300" src="https://raw.githubusercontent.com/maximiliancw/crawlio/master/static/logo.png" alt="crawlio">

# crawlio
Simple website crawler built with Python's `asyncio`


## Features

- Asynchronous "deep" crawling using `asyncio`, `aiohttp` and `Parsel` (by Scrapy authors)
- Zero-configuration
- Customizable XPath selectors

## Setup
```bash
pip install crawlio
```

## Usage

### Synchronous ()
```python
import asyncio
from crawlio import Crawler

fields = {
    'title': '/html/head/title/text()',
    # ...
}
crawler = Crawler('https://quotes.toscrape.com/', selectors=fields)
results = asyncio.run(crawler.run(), debug=True)
for item in results:
    print(item)
```

### Asynchronous
```python
import asyncio
from crawlio import Crawler

async def some_coroutine():
    fields = {
        'title': '/html/head/title/text()',
        # ...
    }
    loop = asyncio.get_event_loop()
    crawler = Crawler('https://quotes.toscrape.com/', selectors=fields)
    results = await crawler.run()
    return results
```


## Contribute
...


# License
...