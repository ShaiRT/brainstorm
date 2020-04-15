import brainstorm.server.server as server
from pathlib import Path
import bson
import pytest
import os


def test_save_blobs_datetime(user, snapshot, tmp_path):
    snapshot['user'] = user
    server.save_blobs(snapshot, path=tmp_path)
    assert type(snapshot['datetime']) == float
    assert type(snapshot['user']['birthday']) == float


def compute_path(path, snapshot):
    date = snapshot['datetime']
    time_format = '%Y-%m-%d_%H-%M-%S-%f'
    time_stamp = date.strftime(time_format)
    user_id = snapshot['user']['user_id']
    path = Path(path).absolute() / str(user_id) / time_stamp
    return path
    

def test_save_blobs_paths(user, snapshot, tmp_path):
    snapshot['user'] = user
    color_image_path = compute_path(tmp_path, snapshot) / 'color_image'
    depth_image_path = compute_path(tmp_path, snapshot) / 'depth_image'    
    server.save_blobs(snapshot, path=tmp_path)
    assert 'path' in snapshot['color_image']
    assert 'path' in snapshot['depth_image']
    assert snapshot['color_image']['path'] == str(color_image_path)
    assert snapshot['depth_image']['path'] == str(depth_image_path)


def test_save_blobs_no_data(user, snapshot, tmp_path):
    snapshot['user'] = user
    server.save_blobs(snapshot, path=tmp_path)
    assert 'data' not in snapshot['color_image']
    assert 'data' not in snapshot['depth_image']
    

def test_save_blobs(user, snapshot, tmp_path):
    snapshot['user'] = user
    color_image_path = compute_path(tmp_path, snapshot) / 'color_image'
    depth_image_path = compute_path(tmp_path, snapshot) / 'depth_image'
    server.save_blobs(snapshot, path=tmp_path)
    assert color_image_path.exists()
    assert depth_image_path.exists()


snapshot_post = None


def mock_publish(data):
    global snapshot_post
    snapshot_post = data


@pytest.fixture
def mock_save_blobs(monkeypatch):
    def mock_save(snapshot, path):
        pass
    monkeypatch.setattr(server,'save_blobs', mock_save)


def test_handle_snapshot(snapshot, user, mock_save_blobs):
    server.server.config['publish'] = mock_publish
    server.server.config['path'] = '.'
    snapshot['user'] = user
    response = server.server.test_client().post('/snapshot', data=bson.encode(snapshot), 
                                                headers={'Connection': 'close'})
    assert response.status_code == 200
    assert snapshot_post == snapshot




'''
def test_publish_to_queue(snapshot_no_blobs):
    pass


def publish_to_queue(snapshot, *, url):
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






"""Tests for RabbitMQ fixtures."""
from rabbitpy import Exchange, Queue

from pytest_rabbitmq.factories.client import clear_rabbitmq


def test_rabbitmq_clear_exchanges(rabbitmq, rabbitmq_proc):
    channel = rabbitmq.channel()
    exchange = Exchange(channel, 'cache-in')
    exchange.declare()
    queue = Queue(channel, 'fastlane')
    queue.declare()
    clear_rabbitmq(rabbitmq_proc, rabbitmq)




    params = pika.ConnectionParameters(host=host, port=port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='snapshots', exchange_type='fanout')
    channel.queue_declare(queue=name)
    channel.queue_bind(exchange='snapshots', queue=name)
    channel.basic_qos(prefetch_count=1)
    callback = ft.partial(parse_and_publish, host=host, port=port, parser=name)
    channel.basic_consume(queue=name, on_message_callback=callback)
    channel.start_consuming()
'''