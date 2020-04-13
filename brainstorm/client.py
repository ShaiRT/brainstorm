"""A client that sends snapshots to a server
"""
import bson
import click
import furl
import requests

import brainstorm.reader as reader


@click.group()
def client_cli():
    pass


def upload_sample(path, host='127.0.0.1', port=8000, reader_driver='protobuf'):
    '''Upload a sample in given path to the server
    The snapshots are POSTed to http://host:port/snapshot in bson format
    
    Arguments:
        path {str} -- the path of the sample file
    
    Keyword Arguments:
        host {str} -- ip address of the server (default: {'127.0.0.1'})
        port {number} -- the server port (default: {8000})
        reader_driver {str} -- a driver for the sample reader (from brainstorm.reader_drivers) (default: {'protobuf'})
    
    Raises:
        ConnectionError -- when communication to the server fails
    '''
    print('running client')
    my_reader = reader.Reader(path, driver=reader_driver)
    print('created reader')
    for snapshot in my_reader:
        print('user:', my_reader.user)
        snapshot['user'] = my_reader.user
        url = furl.furl(scheme='http', host=host,
                        port=port, path='snapshot').url
        print('posting')
        r = requests.post(url=url, data=bson.encode(snapshot),
                          headers={'Connection': 'close'})
        print('posted')
        if not r.status_code == 200:
            raise ConnectionError(f'Upload failed with status code: {r.status_code}')
        r.close()


@client_cli.command('upload-sample')
@click.option('host', '-h', '--host', default='127.0.0.1', show_default=True)
@click.option('port', '-p', '--port', default=8000, show_default=True)
@click.option('reader_driver', '-rd', '--reader-driver', default='protobuf', show_default=True)
@click.argument('path')
def cli_upload_sample(path, host='127.0.0.1', port=8000, reader_driver='protobuf'):
    upload_sample(path=path, host=host, port=port, reader_driver=reader_driver)



if __name__ == '__main__':
    client_cli()
