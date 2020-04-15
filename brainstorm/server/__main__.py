import click

from brainstorm.server.server import run_server_with_queue


@click.group()
def server_cli():
    pass


@server_cli.command('run-server')
@click.option('host', '-h', '--host', default='127.0.0.1', show_default=True)
@click.option('port', '-p', '--port', default=8000, show_default=True)
@click.option('path', '--path', default='data', show_default=True)
@click.argument('url')
def run_server(url, *, host='127.0.0.1', port=8000, path='data'):
    '''run the server to recieve snapshots
    and post to a message queue

    Arguments:
        url {[type]} -- the message queue url

    Keyword Arguments:
        host {str} -- the server host (default: {'127.0.0.1'})
        port {int} -- the server port (default: {8000})
        path {str} -- directory for blob storage (default: {'data'})
    '''
    run_server_with_queue(url=url, host=host, port=port, path=path)


if __name__ == '__main__':
    server_cli()
