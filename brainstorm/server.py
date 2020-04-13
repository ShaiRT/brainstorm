"""A server that recieves samples from clients.
"""
import bson
import click
import flask
import functools as ft
import furl
import json
import logging
import os
import pika

from pathlib import Path


'''# this code will suppress flask messages:
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)'''
os.environ['WERKZEUG_RUN_MAIN'] = 'true'


server = flask.Flask('brainstorm')


@click.group()
def server_cli():
    pass


@server.route("/shutdown", methods=['POST'])
def shutdown_server():
    """This function shuts down the server.

    Returns:
        200 OK

    Raises:
        RuntimeError: shutdown failed
    """
    # TODO: add username and password for shutdown?
    shutdown = flask.request.environ.get('werkzeug.server.shutdown')
    if shutdown is None:
        raise RuntimeError('server shutdown failed')
    shutdown()
    return '', 200


@server.route('/snapshot', methods=['POST'])
def handle_snapshot():
    """Handle a snapshot that arrived.

    Returns:
        200 OK
    """
    snapshot = bson.decode(flask.request.get_data())
    save_blobs(snapshot)
    server.config['publish'](snapshot)
    return '', 200


def save_blobs(snapshot):
    """Save color and depth image of snapshot

    Args:
        snapshot (dict): the snapshot
    """
    date = snapshot['datetime']
    time_format = '%Y-%m-%d_%H-%M-%S-%f'
    time_stamp = date.strftime(time_format)
    user_id = snapshot['user']['user_id']
    path = Path().absolute() / 'data' / str(user_id) / time_stamp
    path.mkdir(parents=True, exist_ok=True)
    color_image_path = path / 'color_image'
    depth_image_path = path / 'depth_image'
    color_image_path.write_bytes(snapshot['color_image']['data'])
    depth_image_path.write_bytes(snapshot['depth_image']['data'])
    del snapshot['color_image']['data']
    del snapshot['depth_image']['data']
    snapshot['color_image']['path'] = str(color_image_path)
    snapshot['depth_image']['path'] = str(depth_image_path)
    snapshot['user']['birthday'] = snapshot['user']['birthday'].timestamp()
    snapshot['datetime'] = snapshot['datetime'].timestamp() * 1000


def publish_to_queue(snapshot, *, url):
    """Publish the snapshot to the message queue

    Args:
        snapshot (dict): the snapshot
        url (string): the message queue url
    """
    f = furl.furl(url)
    host = f.host
    port = f.port
    params = pika.ConnectionParameters(host=host, port=port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='snapshots', exchange_type='fanout')
    channel.basic_publish(exchange='snapshots',
                          routing_key='', body=json.dumps(snapshot))
    connection.close()


def run_server(host='127.0.0.1', port=8000, publish=print):
    """Summary

    Args:
        host (str, optional): Description
        port (int, optional): Description
        publish (TYPE, optional): Description
    """
    global server
    server.config['publish'] = publish
    server.run(host=host, port=port, debug=False, threaded=True)


@server_cli.command('run-server')
@click.option('host', '-h', '--host', default='127.0.0.1', show_default=True)
@click.option('port', '-p', '--port', default=8000, show_default=True)
@click.argument('url')
def run_server_with_queue(url, host='127.0.0.1', port=8000):
    """Summary

    Args:
        url (TYPE): Description
        host (str, optional): Description
        port (int, optional): Description
    """
    publish = ft.partial(publish_to_queue, url=url)
    run_server(host=host, port=port, publish=publish)


if __name__ == '__main__':
    server_cli()
