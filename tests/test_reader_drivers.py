import PIL.Image
import brainstorm.reader_drivers as drivers
import google.protobuf.json_format as pb_json
import inspect
import numpy as np
import pytest
import stringcase as sc
import struct

from brainstorm.reader_drivers.sample_pb2 import Snapshot
from brainstorm.reader_drivers.sample_pb2 import User


def test_import():
    """Test the dynamic importing of the module
    """
    assert type(drivers) == dict
    for key, val in drivers.items():
        assert inspect.isclass(val)
        assert val.__name__.endswith('Driver')
        assert key + '_driver' == sc.snakecase(val.__name__)


def generate_binary_sample(user, snapshot):
    sample = []
    sample.append(struct.pack('<QI', user['user_id'], len(user['username'])))
    username = user['username']
    sample.append(struct.pack(f'{len(username)}s', username.encode()))
    sample.append(struct.pack('<Ic', int(user['birthday'].timestamp()), user['gender'][0].encode()))
    sample.append(struct.pack('<Q', int(snapshot['datetime'].timestamp() * 1000)))
    sample.append(struct.pack('7d', *snapshot['pose']['translation'].values(), *snapshot['pose']['rotation'].values()))
    sample.append(struct.pack('<II', snapshot['color_image']['height'], snapshot['color_image']['width']))
    color_image_data = PIL.Image.frombytes('RGB', (snapshot['color_image']['width'], snapshot['color_image']['height']), snapshot['color_image']['data'])
    data = np.asarray(color_image_data)
    color_image_data = PIL.Image.fromarray(np.flip(data, axis=2))
    sample.append(color_image_data.tobytes())
    sample.append(struct.pack('<II', snapshot['depth_image']['height'], snapshot['depth_image']['width']))
    sample.append(snapshot['depth_image']['data'])
    sample.append(struct.pack('4f', *snapshot['feelings'].values()))
    return b''.join(sample)


def generate_protobuf_sample(user, snapshot):
    tmp_user = dict(user)
    tmp_snapshot = dict(snapshot)
    tmp_user['birthday'] = user['birthday'].timestamp()
    tmp_snapshot['datetime'] = snapshot['datetime'].timestamp() * 1000

    tmp_snapshot['color_image'] = dict(snapshot['color_image'])
    tmp_snapshot['color_image']['data'] = b''
    tmp_snapshot['depth_image'] = dict(snapshot['depth_image'])
    tmp_snapshot['depth_image']['data'] = []

    genders = {'male': 0, 'female': 1, 'other': 2}
    tmp_user['gender'] = genders[user['gender']]
    pb_user = User()
    pb_user = pb_json.ParseDict(tmp_user, pb_user, ignore_unknown_fields=True)
    pb_snapshot = Snapshot()
    pb_snapshot = pb_json.ParseDict(tmp_snapshot, pb_snapshot, ignore_unknown_fields=True)

    pb_snapshot.color_image.data = snapshot['color_image']['data']
    pb_snapshot.depth_image.data[:] = np.frombuffer(snapshot['depth_image']['data'], 'f')
    user_bytes = pb_user.SerializeToString()

    snapshot_bytes = pb_snapshot.SerializeToString()
    sample = struct.pack('<I', len(user_bytes)) + user_bytes
    sample += struct.pack('<I', len(snapshot_bytes)) + snapshot_bytes
    return sample


@pytest.mark.parametrize('generate, driver', [
    (generate_binary_sample, 'binary'),
    (generate_protobuf_sample, 'protobuf'),
    ])
def test_driver(generate, driver, tmp_path, user, snapshot):
    path = tmp_path / 'sample.mind'
    path.write_bytes(generate(user, snapshot))
    d = drivers[driver](str(path))
    driver_user = d.get_user()
    driver_snapshot = d.get_snapshot()
    assert driver_user == user
    assert driver_snapshot == snapshot
