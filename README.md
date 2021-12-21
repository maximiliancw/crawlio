# crawlio
Asynchronous web crawling and scraping with Python for minimalists

> Warning: this project is under active development and **not yet production-ready**!

## Features

- Crawling: download an entire website in just a few seconds
- Scraping: Customizable XPath & CSS data selectors (using `parsel`)
- Zero-configuration: get up and running with ~5 LoC
- Interfaces: Web UI + JSON API powered by FastAPI & VueJS

Built with `asyncio`, `aiohttp` and 🍺

## Setup
```bash
pip install crawlio
```

## Usage

```python
import asyncio
from crawlio import Crawler, Selector

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
```

## License
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