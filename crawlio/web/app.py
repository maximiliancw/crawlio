import uvicorn as uvicorn
from fastapi import FastAPI, APIRouter, Body
from fastapi.responses import HTMLResponse
from pydantic.networks import AnyHttpUrl

from crawlio import Crawler

app = FastAPI()

api = APIRouter(prefix='/api')


@app.get("/", response_class=HTMLResponse)
async def read_items():
    return """
    <!doctype html>
    <html lang="en" style="height: 100%">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://unpkg.com/@picocss/pico@latest/css/pico.min.css">
        <title>crawl.io</title>
        <script src="https://cdn.jsdelivr.net/npm/vue@2"></script>
        <style>
            span.selector {
                text-align: center;
                max-width:30%;
                margin: 10px 0;
                color: darkgrey;
                padding: 15px 40px;
                border: 1px solid darkgrey;
                border-radius: 30px;
            }
            span.selector:hover {
                background-color: red;
                color: white;
            }
            
            code {
                padding: 5px 5px;
                color: darkgrey;
            }
        </style>
      </head>
      <body>
        <main id="app" class="container">
          <nav>
            <ul>
                <li>crawl.io</li>
                <li><a href="#">Docs</a></li>
                <li><a href="#">Source</a></li>
            </ul>
          </nav>
          <div style="padding: 50px 0; margin-bottom: 100px; border-top: 1px solid grey; border-bottom: 1px solid grey">
            <input v-model="url" id="url" placeholder="http://example.com" />
            <span>Selectors</span>
            <div class="grid">
                <input v-model="selector.name" placeholder="Field Name" />
                <input v-model="selector.query" placeholder="XPath" />
                <button v-on:click="addSelector()">+</button>
            </div>
            <div style="margin: 50px 0;">
                <span 
                    class="selector" 
                    v-for="(s, i) in selectors" v-bind:key="i"
                    v-on:click="delSelector(s)"
                    title="X Delete"
                >
                    {{ s.name }}: <code>{{ s.query }}</code>
                </span>
            </div>
            <button>CRAWL</button>
          </div>
          <table v-if="rows.length">
            <thead>
                <tr>
                    <th>URL</th>
                    <th>Headers</th>
                    <th>Data</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(row, i) in rows" v-bind:key="i">
                    <td v-for="key in Object.keys(row)" v-bind:key="key">
                        {{ row[key] }}
                    </td>
                </tr>
            </tbody>
          </table>
        </main>
        <script>
            var app = new Vue({
                el: '#app',
                data() {
                    return {
                        url: '',
                        selectors: [],
                        selector: { name: '', query: '' },
                        columns: [
                            {},
                        ],
                        rows: []
                    }
                },
                methods: {
                    addSelector() {
                        this.selectors.push(Object.assign({}, this.selector))
                        this.selector.name = ''
                        this.selector.query = ''
                    },
                    delSelector(selector) {
                        this.selectors = this.selectors.filter(s => selector !== s)
                    }
                }
            });
        </script>
      </body>
    </html>
    """


@app.post('/')
async def crawl(url: AnyHttpUrl = Body(...)):
    crawler = Crawler(url)
    return crawler.run()


if __name__ == '__main__':
    uvicorn.run(app)

