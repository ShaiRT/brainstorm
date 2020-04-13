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
#os.environ['WERKZEUG_RUN_MAIN'] = 'true'


server = flask.Flask(__name__)



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
    return '', 200



@server.route('/')
def index():
    return 'hello'


server.run(host='127.0.0.1', port=6000, debug=False, threaded=True)
