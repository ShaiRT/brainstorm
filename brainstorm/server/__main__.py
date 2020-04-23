import blessings
import click
import sys
import traceback

from brainstorm.server.server import run_server_with_queue


@click.group()
def server_cli():
    pass


@server_cli.command('run-server')
@click.option('host', '-h', '--host', default='127.0.0.1', show_default=True)
@click.option('port', '-p', '--port', default=8000, show_default=True)
@click.option('path', '--path', default='data', show_default=True)
@click.argument('url')
@click.option('tb', '-t', '--traceback', is_flag=True, default=False, show_default=True)
def run_server(url, *, host='127.0.0.1', port=8000, path='data', tb=False):
    '''run the server to recieve snapshots
    and post to a message queue

    Arguments:
        url {[type]} -- the message queue url

    Keyword Arguments:
        host {str} -- the server host (default: {'127.0.0.1'})
        port {int} -- the server port (default: {8000})
        path {str} -- directory for blob storage (default: {'data'})
    '''
    try:
        run_server_with_queue(url=url, host=host, port=port, path=path)
    except Exception as e:
        track = traceback.format_exc()
        t = blessings.Terminal()
        if tb:
            click.echo(t.red(track))
        else:
            click.echo(t.red(f'Failed with exception {type(e).__name__}: \n{e}'))
        sys.exit(1)


if __name__ == '__main__':
    server_cli()
