import brainstorm.client as client
import brainstorm.reader as reader
import flask
import pytest


import bson
import flask
import functools as ft
import furl
import json
import logging
import os
import pika
import requests

from pathlib import Path

PORT = 6000
HOST = 'localhost'


class MockReader():
    def __init__(self, path, driver):
        print('i am mock reader')

    def __iter__(self):
        yield self.snapshot

@pytest.fixture
def mock_reader(user, snapshot, monkeypatch):
    MockReader.user = user
    MockReader.snapshot = snapshot
    monkeypatch.setattr(reader, 'Reader', MockReader)




'''
# this code will suppress flask messages:
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
os.environ['WERKZEUG_RUN_MAIN'] = 'true'
'''

mock_server = flask.Flask('brainstorm')

@mock_server.route("/shutdown", methods=['POST'])
def shutdown_mock_server():
    shutdown = flask.request.environ.get('werkzeug.mock_server.shutdown')
    if shutdown is None:
        raise RuntimeError('mock_server shutdown failed')
    shutdown()
    return '', 200

@mock_server.route('/')
def handle_index():
    return 'hello', 200


@mock_server.route('/snapshot', methods=['POST'])
def handle_snapshot():
    print('yay')
    #snapshot = bson.decode(flask.request.get_data())
    #mock_server.config['publish'](snapshot)
    return '', 200

@pytest.fixture
def run_mock_server():
    print('in server fixture')
    global mock_server
    mock_server.config['publish'] = print
    mock_server.run(host=HOST, port=PORT, debug=False, threaded=True)
    print('server is running')


def test_client(mock_reader, run_mock_server):
    print('testing...')
    client.upload_sample('.', host=HOST, port=PORT)
    assert True

