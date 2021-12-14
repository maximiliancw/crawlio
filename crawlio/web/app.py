from typing import Dict, List

import uvicorn as uvicorn
from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic.networks import AnyHttpUrl

from crawlio import Crawler

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get("/")
async def index():
    return FileResponse('index.html')


@app.post('/crawl')
async def crawl(url: AnyHttpUrl = Body(...), selectors: Dict[str, str] = Body(None)):
    crawler = Crawler(url, selectors)
    return await crawler.run()


if __name__ == '__main__':
    uvicorn.run(app)
