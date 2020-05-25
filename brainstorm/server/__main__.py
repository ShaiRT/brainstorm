import blessings
import click
import sys
import traceback

from .server import run_server_with_queue


@click.group()
def server_cli():
    pass


@server_cli.command('run-server')
@click.option('host', '-h', '--host', default='127.0.0.1',
              show_default=True, help='the server host')
@click.option('port', '-p', '--port', default=8000,
              show_default=True, help='the server port')
@click.option('path', '--path', default='data',
              show_default=True, help='directory for blob storage')
@click.option('tb', '-t', '--traceback', is_flag=True, default=False,
              show_default=True, help='show full traceback on failure')
@click.argument('url')
def run_server(url, *, host='127.0.0.1', port=8000, path='data', tb=False):
    '''run the server to recieve snapshots
    and post to a message queue in given url.
    '''
    try:
        run_server_with_queue(url=url, host=host, port=port, path=path)
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
    server_cli()
