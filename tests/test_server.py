import brainstorm.server.server as server
import bson
import json
import os
import pytest

from pathlib import Path


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


def test_handle_snapshot(snapshot_no_blobs, user, mock_save_blobs):
    snapshot = snapshot_no_blobs
    server.server.config['publish'] = mock_publish
    server.server.config['path'] = '.'
    snapshot['user'] = user
    snapshot['datetime'] = snapshot['datetime'].timestamp()
    snapshot['user']['birthday'] = snapshot['user']['birthday'].timestamp()
    response = server.server.test_client().post('/snapshot', data=bson.encode(snapshot), 
                                                headers={'Connection': 'close'})
    assert response.status_code == 200
    assert json.loads(snapshot_post) == snapshot
