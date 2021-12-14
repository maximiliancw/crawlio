import asyncio

import click as click

from crawlio import Crawler


@click.group(invoke_without_command=True)
def cli():
    pass


@cli.command()
@click.argument('url')
@click.option('-e', '--export', type=bool)
def run(url: str):
    crawler = Crawler(url)
    output = asyncio.run(crawler.run())
    print(output)


if __name__ == '__main__':
    cli()

