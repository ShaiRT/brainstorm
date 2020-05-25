import blessings
import click
import furl
import json
import requests
import sys
import traceback

from prettytable_extras import PrettyTable
from functools import wraps


@click.group()
def cli():
    pass


def perror(f):
    @click.option('tb', '-t', '--traceback',
                  is_flag=True, default=False, show_default=True,
                  help='show full traceback on failure')
    @wraps(f)
    def wrapper(tb=False, *args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as e:
            t = blessings.Terminal()
            if tb:
                track = traceback.format_exc()
                click.echo(t.red(track))
            else:
                click.echo(t.red(
                    f'Failed with exception {type(e).__name__}: \n{e}'))
            sys.exit(1)
    return wrapper


@cli.command()
@click.option('host', '-h', '--host', default='127.0.0.1',
              show_default=True, help='the api host')
@click.option('port', '-p', '--port', default=5000,
              show_default=True, help='the api port')
@perror
def get_users(host='127.0.0.1', port=5000):
    '''Print a list of IDs and names of all supported users.
    '''
    url = furl.furl(scheme='http', host=host, port=port, path='users').url
    response = requests.get(url)
    users = response.json()
    table = PrettyTable(["user_id", "username"], header_color='blue,bold',
                        left_padding_width=3, right_padding_width=3)
    table.sortby = "user_id"
    for user in users:
        table.add_row([user['user_id'], user['username']])
    click.echo(table)


@cli.command()
@click.argument('user_id')
@click.option('host', '-h', '--host', default='127.0.0.1',
              show_default=True, help='the api host')
@click.option('port', '-p', '--port', default=5000,
              show_default=True, help='the api port')
@perror
def get_user(user_id, host='127.0.0.1', port=5000):
    '''Print the specified user’s details: ID, name, birthday and gender.
    '''
    url = furl.furl(scheme='http', host=host, port=port)
    url.path.segments = ['users', user_id]
    response = requests.get(url.url)
    if response.status_code == 404:
        return None
    user = response.json()
    t = blessings.Terminal()
    click.echo(t.bold_blue(f"user {user['user_id']}") +
               f": {user['username']}, born {user['birthday']}" +
               t.dim(f" ({user['gender']})"))


@cli.command('get-snapshots')
@click.argument('user_id')
@click.option('host', '-h', '--host', default='127.0.0.1',
              show_default=True, help='the api host')
@click.option('port', '-p', '--port', default=5000,
              show_default=True, help='the api port')
@perror
def get_user_snapshots(user_id, host='127.0.0.1', port=5000):
    '''Print a list of the specified user’s snapshot IDs and datetimes.
    '''
    url = furl.furl(scheme='http', host=host, port=port)
    url.path.segments = ['users', user_id, 'snapshots']
    response = requests.get(url.url)
    snapshots = response.json()
    table = PrettyTable(["snapshot_id", "datetime"], header_color='green,bold',
                        left_padding_width=3, right_padding_width=3)
    table.sortby = "snapshot_id"
    for snapshot in snapshots:
        table.add_row([snapshot['snapshot_id'], snapshot['datetime']])
    click.echo(table)


@cli.command()
@click.argument('user_id')
@click.argument('snapshot_id')
@click.option('host', '-h', '--host', default='127.0.0.1',
              show_default=True, help='the api host')
@click.option('port', '-p', '--port', default=5000,
              show_default=True, help='the api port')
@perror
def get_snapshot(user_id, snapshot_id, host='127.0.0.1', port=5000):
    '''Print the specified snapshot’s details:
    ID, datetime, and the available results’ names.
    '''
    url = furl.furl(scheme='http', host=host, port=port)
    url.path.segments = ['users', user_id, 'snapshots', snapshot_id]
    response = requests.get(url.url)
    if response.status_code == 404:
        return None
    snapshot = response.json()
    t = blessings.Terminal()
    click.echo(t.bold_green(f"Snapshot {snapshot['snapshot_id']}") +
               f": {snapshot['datetime']}.")
    click.echo(t.green(f"Available results") +
               f": {', '.join(snapshot['available_results'])}")


@cli.command('get-result')
@click.argument('user_id')
@click.argument('snapshot_id')
@click.argument('result_name')
@click.option('host', '-h', '--host', default='127.0.0.1',
              show_default=True, help='the api host')
@click.option('port', '-p', '--port', default=5000,
              show_default=True, help='the api port')
@click.option('path', '-s', '--save', default=None, help='path to save data')
@perror
def get_snapshot_result(user_id, snapshot_id, result_name,
                        host='127.0.0.1', port=5000, path=None):
    '''Print the specified snapshot’s result (if available).
    When given a path, the result is saved to the path in json format
    instead of being printed.
    '''
    url = furl.furl(scheme='http', host=host, port=port)
    url.path.segments = ['users', user_id,
                         'snapshots', snapshot_id, result_name]
    response = requests.get(url.url)
    if response.status_code == 404:
        return None
    data = response.json()
    if path is None:
        t = blessings.Terminal()
        data_string = '\n'.join([t.green(key) +
                                f": {val}" for key, val in data.items()])
        click.echo(data_string)
        return
    with open(path, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    cli()
