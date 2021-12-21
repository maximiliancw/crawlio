import asyncio

import click as click

from crawlio import Crawler


@click.group(invoke_without_command=True)
def cli():
    pass


@cli.command()
@click.argument('url')
@click.option('-e', '--export', type=bool, default=False)
def run(url: str, export: bool = False):
    crawler = Crawler(url)
    output = asyncio.run(crawler.run())
    if not export:
        print('-----------\nStats:')
        for key, value in output['info'].items():
            print(key, ': ', value)
        print('-----------\nResults:')
        for page in output['data']:
            print('\n')
            for key, value in page.items():
                print(key, '\t', value)
    else:
        # TODO: Implement export functionality
        pass
