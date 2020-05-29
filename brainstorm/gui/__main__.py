import blessings
import click
import sys
import traceback

from .gui_server import run_server


@click.group()
def gui_cli():
    pass


@gui_cli.command('run-server')
@click.option('host', '-h', '--host', default='127.0.0.1',
              show_default=True, help='the gui server host')
@click.option('port', '-p', '--port', default=8080,
              show_default=True, help='the gui server port')
@click.option('api_host', '-H', '--api-host', default='127.0.0.1',
              show_default=True, help='the api server host')
@click.option('api_port', '-P', '--api-port', default=5000,
              show_default=True, help='the api server port')
@click.option('tb', '-t', '--traceback', is_flag=True, default=False,
              show_default=True, help='show full traceback on failure')
def cli_run_server(host='127.0.0.1', port=8080,
                   api_host='127.0.0.1', api_port=5000, tb=False):
    '''Run the gui server at 'http://host:port'
    The gui server displays the information exposed by the api server.
    '''
    try:
        run_server(host=host, port=port, api_host=api_host, api_port=api_port)
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
    gui_cli()
