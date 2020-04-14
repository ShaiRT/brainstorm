import click

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
    print(reader)
    for snapshot in reader:
        date = snapshot['datetime'].strftime('%B%e, %Y')
        time = snapshot['datetime'].strftime('%H:%M:%S.%f')
        print(f'Snapshot from {date} at {time}')


@client_cli.command('upload-sample')
@click.option('host', '-h', '--host', default='127.0.0.1', show_default=True)
@click.option('port', '-p', '--port', default=8000, show_default=True)
@click.option('reader_driver', '-rd', '--reader-driver',
              default='protobuf', show_default=True)
@click.argument('path')
def cli_upload_sample(path, *, host='127.0.0.1', port=8000,
                      reader_driver='protobuf'):
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

    Raises:
        ConnectionError -- when communication to the server fails
    '''
    upload_sample(path=path, host=host, port=port, reader_driver=reader_driver)


client_cli()
