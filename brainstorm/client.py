import click
from brainstorm.utils import Reader
import requests
import furl
import bson


@click.group()
def client_cli():
    pass


@client_cli.command('upload-sample')
@click.option('host', '-h', '--host', default='127.0.0.1', show_default=True)
@click.option('port', '-p', '--port', default=8000, show_default=True)
@click.argument('path')
def upload_sample(path, host='127.0.0.1', port=8000):
    reader = Reader(path)
    for snapshot in reader:
        snapshot['user'] = reader.user
        url = furl.furl(scheme='http', host='127.0.0.1',
                        port=8000, path='snapshot').url
        r = requests.post(url=url, data=bson.encode(snapshot),
                          headers={'Connection': 'close'})
        if not r.status_code == 204:
            raise ConnectionError(f'Response status code: {r.status_code}')
        r.close()


if __name__ == '__main__':
    client_cli()
