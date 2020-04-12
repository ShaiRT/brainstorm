"""A driver that converts a sample
from a protobuf format to a dictionary format
"""
import datetime as dt
import google.protobuf.json_format as pb_json
import gzip
import struct

from brainstorm.reader_drivers.sample_pb2 import Snapshot
from brainstorm.reader_drivers.sample_pb2 import User


class ProtobufDriver:
    '''A driver to convert sample formats

    The sample must be a binary (possibly gzipped),
    with a sequence of message sizes (uint32) and messages (of that size),
    where the first one is a User message,
    and the rest are Snapshot messages, as defined in 'sample.proto'.

    Implements the interface required by brainstorm.reader.Reader

    '''

    genders = {0: 'male', 1: 'female', 2: 'other'}

    def __init__(self, path):
        '''
        Arguments:
            path {string} -- path to a '.mind' or '.mind.gz' file
        '''
        self.path = path
        self._offset = 0
        self.user = None
        self.open = gzip.open if path.endswith('.gz') else open

    def get_user(self):
        '''
        Returns:
            dict -- user of the sample
        '''
        if self.user is not None:
            return self.user

        with self.open(self.path, 'rb') as sample:
            size, = struct.unpack('<I', sample.read(4))
            user = User()
            user.ParseFromString(sample.read(size))
            self._offset = sample.tell()

        self.user = dict()
        self.user['user_id'] = user.user_id
        self.user['username'] = user.username
        self.user['birthday'] = dt.datetime.fromtimestamp(user.birthday)
        self.user['gender'] = self.genders[user.gender]
        return self.user

    def get_snapshot(self):
        '''get the next snapshot from the sample

        assumes self.get_user has been called previously

        Returns:
            dict -- the snapshot as a dictionary
        '''
        with self.open(self.path, 'rb') as sample:
            sample.seek(self._offset, 0)
            size_bytes = sample.read(4)
            if not size_bytes:
                return None
            size, = struct.unpack('<I', size_bytes)
            snapshot = Snapshot()
            snapshot.ParseFromString(sample.read(size))
            self._offset = sample.tell()

        datetime = dt.datetime.fromtimestamp(snapshot.datetime / 1000.0)
        color_image_data = snapshot.color_image.data

        depth_image = snapshot.depth_image
        serialized = depth_image.SerializeToString()
        depth_image_size = depth_image.width * depth_image.height
        metadata = len(serialized) - (4 * depth_image_size)
        depth_image_data = serialized[metadata:]

        snapshot = pb_json.MessageToDict(snapshot,
                                         preserving_proto_field_name=True)
        snapshot['datetime'] = datetime
        snapshot['color_image']['data'] = color_image_data
        snapshot['depth_image']['data'] = depth_image_data
        return snapshot
