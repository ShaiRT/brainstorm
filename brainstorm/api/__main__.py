import blessings
import click
import sys
import traceback

from .api import run_api_server


@click.group()
def api_cli():
    pass


@api_cli.command('run-server')
@click.option('host', '-h', '--host', default='127.0.0.1',
              show_default=True, help='the servers host')
@click.option('port', '-p', '--port', default=5000,
              show_default=True, help='the servers port')
@click.option('database_url', '-d', '--database',
              default='mongodb://localhost:27017',
              show_default=True, help='the url of the database')
@click.option('tb', '-t', '--traceback', is_flag=True,
              default=False, show_default=True,
              help='show full traceback on failure')
def run_server(host='127.0.0.1', port=5000,
               database_url='mongodb://localhost:27017', tb=False):
    '''Run the api server to respond to http requests
    at 'http://host:port' and expose the data in the database.
    '''
    try:
        run_api_server(host=host, port=port, database_url=database_url)
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
    api_cli()
