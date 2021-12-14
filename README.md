<img width="300" src="https://raw.githubusercontent.com/maximiliancw/crawlio/master/static/logo.png" alt="crawlio">

# crawlio
Simple web crawler built with Python's `asyncio`

> Warning: this project is under active development and **not yet production-ready**!

## Features

- Crawling: download an entire website in seconds
- Scraping: Customizable XPath selectors
- Zero-configuration: get up and running with ~5 LoC

Built with `asyncio`, `aiohttp` and `Parsel` (by Scrapy authors)

## Setup
```bash
pip install crawlio
```

## Usage

```python
import asyncio
from crawlio import Crawler

fields = {
    'title': '//title/text()',
    'text': '//p//text()'
}
crawler = Crawler('https://quotes.toscrape.com/', selectors=fields)
output = asyncio.run(crawler.run(), debug=True)
for item in output["results"]:
    print(item)
```


# License
Copyright (C) 2021  Maximilian Wolf

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.