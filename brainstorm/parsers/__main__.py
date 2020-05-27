import blessings
import click
import sys
import traceback

from . import parse_path, run_parser


@click.group()
def parsers_cli():
    pass


@parsers_cli.command('parse')
@click.option('tb', '-t', '--traceback', is_flag=True,
              default=False, show_default=True,
              help='show full traceback on failure')
@click.argument('name')
@click.argument('path')
def cli_parse(name, path, tb=False):
    """parse snapshot data in given path
    with parser with given name and print result
    """
    try:
        click.echo(parse_path(name, path))
    except Exception as e:
        track = traceback.format_exc()
        t = blessings.Terminal()
        if tb:
            click.echo(t.red(track))
        else:
            click.echo(t.red(
                f'Failed with exception {type(e).__name__}: \n{e}'))
        sys.exit(1)


@parsers_cli.command('run-parser')
@click.option('tb', '-t', '--traceback', is_flag=True,
              default=False, show_default=True,
              help='show full traceback on failure')
@click.argument('name')
@click.argument('url')
def cli_run_parser(name, url, tb=False):
    """run parser with given name to listen to message queue in given url,
    parse data, and post back to 'data' topic exchange of the
    message queue with routing_key=name.
    """
    try:
        run_parser(name, url)
    except Exception as e:
        track = traceback.format_exc()
        t = blessings.Terminal()
        if tb:
            click.echo(t.red(track))
        else:
            click.echo(t.red(
                f'Failed with exception {type(e).__name__}: \n{e}'))
        sys.exit(1)


if __name__ == '__main__':
    parsers_cli()
