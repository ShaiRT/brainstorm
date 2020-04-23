import os
import sys
import pytest
import datetime as dt
from pathlib import Path
import inspect
import PIL.Image


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
is_travis = (os.environ.get('TRAVIS') == 'true')


@pytest.fixture
def user():
    user = dict()
    user['user_id'] = 12
    user['username'] = 'Shai Rahat'
    user['birthday'] = dt.datetime(2000, 6, 12)
    user['gender'] = 'female'
    return user


@pytest.fixture
def snapshot_no_blobs():
    snap = dict()
    snap['datetime'] = dt.datetime(2020, 6, 12)
    snap['pose'] = {'translation': {'x': 1, 'y': 2, 'z': 3},
                    'rotation': {'x': 10, 'y': 20, 'z': 30, 'w': 40}}
    snap['feelings'] = {'hunger': -1,
                        'thirst': 0.5,
                        'exhaustion': -0.5,
                        'happiness': 1}
    my_dir = Path(inspect.getsourcefile(lambda: 0)).absolute().parent
    depth_image = PIL.Image.open(my_dir /'my_snapshot_heatmap.jpg').convert('F')
    color_image = PIL.Image.open(my_dir /'my_snapshot_image.jpg')
    snap['depth_image'] = {'width': depth_image.width,'height': depth_image.height}
    snap['color_image'] = {'width': color_image.width,'height': color_image.height}
    return snap


@pytest.fixture
def snapshot(snapshot_no_blobs):
    snap = snapshot_no_blobs
    my_dir = Path(inspect.getsourcefile(lambda: 0)).absolute().parent
    depth_image = PIL.Image.open(my_dir /'my_snapshot_heatmap.jpg').convert('F')
    color_image = PIL.Image.open(my_dir /'my_snapshot_image.jpg')
    snap['depth_image']['data'] = depth_image.tobytes()
    snap['color_image']['data'] = color_image.tobytes()
    return snap


@pytest.fixture(scope='module')
def mongo():
    if not is_travis:
        os.system('docker run --rm -d -p 9867:27017 --name test_mongo mongo')
    yield 'mongodb://127.0.0.1:9867'
    if not is_travis:
        os.system('docker stop test_mongo')


@pytest.fixture(scope='module')
def rabbitmq():
    if not is_travis:
        os.system('docker run --rm -d -p 5672:5672 --name test_rabbitmq rabbitmq')
    yield 'rabbitmq://127.0.0.1:5672'
    if not is_travis:
        os.system('docker stop test_rabbitmq')
