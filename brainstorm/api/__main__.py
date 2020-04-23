import click

from brainstorm.api.api import run_api_server


@click.group()
def api_cli():
    pass


@api_cli.command('run-server')
@click.option('host', '-h', '--host', default='127.0.0.1', show_default=True)
@click.option('port', '-p', '--port', default=5000, show_default=True)
@click.option('database_url', '-d', '--database',
              default='mongodb://localhost:27017', show_default=True)
def run_server(host='127.0.0.1', port=5000, database_url='mongodb://localhost:27017'):
    run_api_server(host=host, port=port, database_url=database_url)


if __name__ == '__main__':
    api_cli()
