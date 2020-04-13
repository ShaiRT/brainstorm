import click
import furl
import json
import requests


@click.group()
def cli():
    pass


@cli.command()
@click.option('host', '-h', '--host', default='127.0.0.1', show_default=True)
@click.option('port', '-p', '--port', default=5000, show_default=True)
def get_users(host='127.0.0.1', port=5000):
    url = furl.furl(scheme='http', host=host, port=port, path='users').url
    response = requests.get(url)
    users = response.json()
    for user in users:
        click.echo(f"user {user['user_id']}: {user['username']}")


@cli.command()
@click.argument('user_id')
@click.option('host', '-h', '--host', default='127.0.0.1', show_default=True)
@click.option('port', '-p', '--port', default=5000, show_default=True)
def get_user(user_id, host='127.0.0.1', port=5000):
    url = furl.furl(scheme='http', host=host, port=port)
    url.path.segments = ['users', user_id]
    response = requests.get(url.url)
    if response.status_code == 404:
        return None
    user = response.json()
    click.echo(f"user {user['user_id']}: {user['username']}, born {user['birthday']} ({user['gender']})")


@cli.command('get-snapshots')
@click.argument('user_id')
@click.option('host', '-h', '--host', default='127.0.0.1', show_default=True)
@click.option('port', '-p', '--port', default=5000, show_default=True)
def get_user_snapshots(user_id, host='127.0.0.1', port=5000):
    url = furl.furl(scheme='http', host=host, port=port)
    url.path.segments = ['users', user_id, 'snapshots']
    response = requests.get(url.url)
    snapshots = response.json()
    for snapshot in snapshots:
        click.echo(f"Snapshot {snapshot['snapshot_id']} from {snapshot['datetime']}")


@cli.command()
@click.argument('user_id')
@click.argument('snapshot_id')
@click.option('host', '-h', '--host', default='127.0.0.1', show_default=True)
@click.option('port', '-p', '--port', default=5000, show_default=True)
def get_snapshot(user_id, snapshot_id, host='127.0.0.1', port=5000):
    url = furl.furl(scheme='http', host=host, port=port)
    url.path.segments = ['users', user_id, 'snapshots', snapshot_id]
    response = requests.get(url.url)
    if response.status_code == 404:
        return None
    snapshot = response.json()
    click.echo(f"Snapshot {snapshot['snapshot_id']} from {snapshot['datetime']}.")
    click.echo(f"Available results: {', '.join(snapshot['available_results'])}")


@cli.command('get-result')
@click.argument('user_id')
@click.argument('snapshot_id')
@click.argument('result_name')
@click.option('host', '-h', '--host', default='127.0.0.1', show_default=True)
@click.option('port', '-p', '--port', default=5000, show_default=True)
@click.option('path', '-s', '--save', default=None)
def get_snapshot_result(user_id, snapshot_id, result_name, host='127.0.0.1', port=5000, path=None):
    url = furl.furl(scheme='http', host=host, port=port)
    url.path.segments = ['users', user_id,
                         'snapshots', snapshot_id, result_name]
    response = requests.get(url.url)
    if response.status_code == 404:
        return None
    data = response.json()
    if path is None:
        click.echo(data)
        return
    with open(path, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    cli()
