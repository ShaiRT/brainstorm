import click
import functools as ft
import furl
import pika

from brainstorm.parsers.__init__ import parse, parse_path, run_parser


@click.group()
def parsers_cli():
    pass


@parsers_cli.command('parse')
@click.argument('name')
@click.argument('path')
def cli_parse(name, path):
    """parse snapshot data in given path
    and print result
    
    Args:
        name (str): the name of the parser to be used
        path (str): the path of data to be parsed
    """
    click.echo(parse_path(name, path))


@parsers_cli.command('run-parser')
@click.argument('name')
@click.argument('url')
def cli_run_parser(name, url):
    """run parser to listen to message queue, parse data,
    and post back to 'data' topic exchange of the 
    message queue with routing_key=name.
    **supports rabbitmq as a message queue
    
    Args:
        name (str): name of the parser to be used
        url (str): url of the message queue
    """
    run_parser(name, url)


if __name__ == '__main__':
    parsers_cli()
