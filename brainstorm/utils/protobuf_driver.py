import gzip
import struct
from brainstorm.utils.sample_pb2 import Snapshot, User
import google.protobuf.json_format as pb_json
import datetime as dt


class ProtobufDriver:

    genders = {0: 'male', 1: 'female', 2: 'other'}

    def __init__(self, path):
        self.path = path
        self._offset = 0
        self.user = None

    def get_user(self):
        if self.user is not None:
            return self.user
        with gzip.open(self.path, 'rb') as sample:
            size, = struct.unpack('<I', sample.read(4))
            user = User()
            user.ParseFromString(sample.read(size))
            self._offset = sample.tell()
        gender = user.gender
        user = pb_json.MessageToDict(user, preserving_proto_field_name=True)
        user['birthday'] = dt.datetime.fromtimestamp(user['birthday'])
        user['gender'] = ProtobufDriver.genders[gender]
        user['user_id'] = int(user['user_id'])
        return user

    def get_snapshot(self):
        with gzip.open(self.path, 'rb') as sample:
            sample.seek(self._offset, 0)
            size_bytes = sample.read(4)
            if not size_bytes:
                return None
            size, = struct.unpack('<I', size_bytes)
            snapshot = Snapshot()
            snapshot.ParseFromString(sample.read(size))
            self._offset = sample.tell()
        datetime = snapshot.datetime
        color_image_data = snapshot.color_image.data
        depth_image_data = snapshot.depth_image.SerializeToString()[10:] # TODO: memoryview?
        snapshot = pb_json.MessageToDict(snapshot,
                                         preserving_proto_field_name=True)
        snapshot['datetime'] = dt.datetime.\
            fromtimestamp(datetime / 1000.0)
        snapshot['color_image']['data'] = color_image_data
        snapshot['depth_image']['data'] = depth_image_data
        return snapshot
