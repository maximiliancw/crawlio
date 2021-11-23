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
```python
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


## Contribute
...


# License
...