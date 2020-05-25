import blessings
import click
import sys
import traceback

from .client import upload_sample
from .reader import Reader


@click.group()
def client_cli():
    pass


@client_cli.command('read')
@click.option('driver', '-d', '--driver',
              default='protobuf', show_default=True,
              help='the name of the driver for the sample - ' +
              'must be a driver from brainstorm.reader_drivers')
@click.argument('path')
def read(path, driver='protobuf'):
    '''Read the sample in given path and print the information.
    '''
    reader = Reader(path, driver=driver)
    click.echo(reader)
    for snapshot in reader:
        date = snapshot['datetime'].strftime('%B%e, %Y')
        time = snapshot['datetime'].strftime('%H:%M:%S.%f')
        click.echo(f'Snapshot from {date} at {time}')


@client_cli.command('upload-sample')
@click.option('host', '-h', '--host', default='127.0.0.1',
              show_default=True, help='ip address of the server')
@click.option('port', '-p', '--port', default=8000,
              show_default=True, help='the server port')
@click.option('reader_driver', '-rd', '--reader-driver',
              default='protobuf', show_default=True,
              help='a driver for the sample reader' +
              '(from brainstorm.reader_drivers)')
@click.option('tb', '-t', '--traceback', is_flag=True,
              default=False, show_default=True,
              help='show full traceback on failure')
@click.argument('path')
def cli_upload_sample(path, *, host='127.0.0.1', port=8000,
                      reader_driver='protobuf', tb=False):
    '''Upload a sample in given path to the server.
    The snapshots are POSTed to http://host:port/snapshot in bson format.
    '''
    t = blessings.Terminal()
    click.echo(t.green('uploading...'))
    try:
        upload_sample(path=path, host=host, port=port,
                      reader_driver=reader_driver)
    except Exception as e:
        track = traceback.format_exc()
        if tb:
            click.echo(t.red(track))
        else:
            click.echo(t.red(
                f'Failed with exception {type(e).__name__}: \n{e}'))
        sys.exit(1)
    click.echo(t.green('done!'))


if __name__ == '__main__':
    client_cli()
