import brainstorm.server.server as server
from pathlib import Path
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


