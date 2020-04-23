import blessings
import click
import sys
import traceback

from brainstorm.client.client import upload_sample
from brainstorm.client.reader import Reader


@click.group()
def client_cli():
    pass


@client_cli.command('read')
@click.option('driver', '-d', '--driver',
              default='protobuf', show_default=True)
@click.argument('path')
def read(path, driver='protobuf'):
    '''Read the sample in path and print the information

    Arguments:
        path {str} -- a path to a sample

    Keyword Arguments:
        driver {str} -- the name of the driver for the sample
                        (default: {'protobuf'})
                        must be a driver from brainstorm.reader_drivers
    '''
    reader = Reader(path, driver=driver)
    click.echo(reader)
    for snapshot in reader:
        date = snapshot['datetime'].strftime('%B%e, %Y')
        time = snapshot['datetime'].strftime('%H:%M:%S.%f')
        click.echo(f'Snapshot from {date} at {time}')


@client_cli.command('upload-sample')
@click.option('host', '-h', '--host', default='127.0.0.1', show_default=True)
@click.option('port', '-p', '--port', default=8000, show_default=True)
@click.option('reader_driver', '-rd', '--reader-driver',
              default='protobuf', show_default=True)
@click.argument('path')
@click.option('tb', '-t', '--traceback', is_flag=True, default=False, show_default=True)
def cli_upload_sample(path, *, host='127.0.0.1', port=8000,
                      reader_driver='protobuf', tb=False):
    '''Upload a sample in given path to the server
    The snapshots are POSTed to http://host:port/snapshot in bson format

    Arguments:
        path {str} -- the path of the sample file

    Keyword Arguments:
        host {str} -- ip address of the server (default: {'127.0.0.1'})
        port {number} -- the server port (default: {8000})
        reader_driver {str} -- a driver for the sample reader
                               (from brainstorm.reader_drivers)
                               (default: {'protobuf'})
    '''
    try:
        upload_sample(path=path, host=host, port=port, reader_driver=reader_driver)
    except Exception as e:
        track = traceback.format_exc()
        t = blessings.Terminal()
        if tb:
            click.echo(t.red(track))
        else:
            click.echo(t.red(f'Failed with exception {type(e).__name__}: \n{e}'))
        sys.exit(1)



if __name__ == '__main__':
    client_cli()
