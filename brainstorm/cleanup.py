import click
import requests
import furl


@click.group()
def cleanup_cli():
    pass


@cleanup_cli.command()
@click.option('host', '-h', '--host', default='127.0.0.1', show_default=True)
@click.option('port', '-p', '--port', default=8000, show_default=True)
def cleanup_server(host='127.0.0.1', port=8000):
    url = furl.furl(scheme='http', host=host,
                    port=port, path='shutdown').url
    r = requests.post(url=url)
    

if __name__ == '__main__':
    cleanup_cli()

