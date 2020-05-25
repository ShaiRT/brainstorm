"""A server that recieves snapshots from clients.
"""
import bson
import flask
import furl
import json
import os
import brainstorm.mq_drivers as mq_drivers

from pathlib import Path


os.environ['WERKZEUG_RUN_MAIN'] = 'true'


server = flask.Flask('brainstorm')


@server.route('/snapshot', methods=['POST'])
def handle_snapshot():
    """Handle a snapshot that arrived.
    Triggered by a POST to /snapshot.
    Assumes the POST contains a snapshot in bson format.

    Returns:
        200 OK
    """
    snapshot = bson.decode(flask.request.get_data())
    save_blobs(snapshot, path=server.config['path'])
    server.config['publish'](json.dumps(snapshot))
    return '', 200


def save_blobs(snapshot, *, path):
    '''Save color and depth image of snapshot
    and convert datetime objects to integers

    Args:
        snapshot (dict): the snapshot
        path (str): path to save the data
    '''
    date = snapshot['datetime']
    time_format = '%Y-%m-%d_%H-%M-%S-%f'
    time_stamp = date.strftime(time_format)
    user_id = snapshot['user']['user_id']
    path = Path(path).absolute() / str(user_id) / time_stamp
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


def run_server(*, host='127.0.0.1', port=8000, publish=print, path='data'):
    '''run the servet at 'http://host:port'

    Keyword Arguments:
        host (str): the server host (default: {'127.0.0.1'})
        port (int): the server port (default: {8000})
        publish (function): function to handle snapshots (default: {print})
        path (str): path to save blobs (default: {'data'})
    '''
    global server
    server.config['publish'] = publish
    server.config['path'] = path
    server.run(host=host, port=port, debug=False, threaded=True)


def run_server_with_queue(url, *, host='127.0.0.1', port=8000, path='data'):
    '''run the server with message queue from mq_drivers.

    Args:
        url (str): message queue url

    Keyword Arguments:
        host (str): server host (default: {'127.0.0.1'})
        port (int): server port (default: {8000})
        path (str): directory for blob storage (default: {'data'})
    '''
    publisher_class = mq_drivers[furl.furl(url).scheme]['publisher']
    publish = publisher_class(url, 'snapshots', 'fanout', '').publish
    run_server(host=host, port=port, publish=publish, path=path)
