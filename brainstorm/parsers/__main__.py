import click
import functools as ft
import furl
import pika

from . import parse, parse_path, run_parser


@click.group()
def parsers_cli():
    pass


@parsers_cli.command('parse')
@click.argument('name')
@click.argument('path')
def cli_parse(name, path):
    """parse snapshot data in given path with parser with given name and print result
    """
    click.echo(parse_path(name, path))


@parsers_cli.command('run-parser')
@click.argument('name')
@click.argument('url')
def cli_run_parser(name, url):
    """run parser with given name to listen to message queue in given url,
    parse data, and post back to 'data' topic exchange of the 
    message queue with routing_key=name.
    """
    run_parser(name, url)


if __name__ == '__main__':
    parsers_cli()
