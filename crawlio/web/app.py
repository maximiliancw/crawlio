from typing import Dict, List

import uvicorn as uvicorn
from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic.networks import AnyHttpUrl

from crawlio import Crawler
from crawlio.classes import Selector

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get("/")
async def index():
    return FileResponse('index.html')


@app.post('/api/crawl')
async def crawl(
        url: AnyHttpUrl = Body(...),
        selectors: List[Selector] = Body(None, description='List of crawlio.Selector instances'),
        delay: float = Body(.3, description='Max. download delay')
):
    crawler = Crawler(url, selectors, delay)
    return await crawler.run()


if __name__ == '__main__':
    uvicorn.run(app)
