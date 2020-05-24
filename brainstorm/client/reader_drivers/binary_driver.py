"""A driver that converts a sample from a binary format to a dictionary format
"""
import PIL.Image
import contextlib
import datetime as dt
import gzip
import struct


class BinaryDriver:
    '''A driver to convert sample formats

    The sample must be a binary (possibly gzipped),
    with a user information and then a list of snapshots.

    Implements the interface required by brainstorm.reader.Reader

    '''

    genders = {'m': 'male', 'f': 'female', 'o': 'other'}

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

        self.user = dict()
        with self.open(self.path, 'rb') as sample:
            self.user['user_id'], username_len = struct.unpack(
                '<QI', sample.read(12))
            username, = struct.unpack(f'<{username_len}s',
                                      sample.read(username_len))
            self.user['username'] = username.decode('utf-8')
            timestamp, = struct.unpack('<I', sample.read(4))
            self.user['birthday'] = dt.datetime.fromtimestamp(timestamp)
            gender, = struct.unpack('<c', sample.read(1))
            self.user['gender'] = self.genders[gender.decode('utf-8')]
            self._offset = sample.tell()
        return self.user

    def bgr_to_rgb(self, image_size, image_bytes):
        '''
        Arguments:
            image_size {(int, int)} -- (width, height)
            image_bytes {bytes} -- image bytes in BGR

        Returns:
            bytes -- image bytes in RGB
        '''
        image = PIL.Image.frombytes(
            'RGB', image_size, image_bytes, 'raw', 'BGR')
        return image.tobytes()

    def get_snapshot(self):
        '''get the next snapshot from the sample

        assumes self.get_user has been called previously

        Returns:
            dict -- the snapshot as a dictionary
        '''
        with self.open(self.path, 'rb') as sample:
            sample.seek(self._offset, 0)
            with contextlib.suppress(struct.error):
                snapshot = dict()

                ms, = struct.unpack('<Q', sample.read(8))
                snapshot['datetime'] = dt.datetime.fromtimestamp(ms / 1000)

                snapshot['pose'] = dict()
                x, y, z = struct.unpack('<3d', sample.read(24))
                snapshot['pose']['translation'] = {'x': x, 'y': y, 'z': z}
                x, y, z, w = struct.unpack('<4d', sample.read(32))
                snapshot['pose']['rotation'] = {'x': x, 'y': y, 'z': z, 'w': w}

                height, width = struct.unpack('<2I', sample.read(8))
                snapshot['color_image'] = {'height': height, 'width': width}
                image_bytes = sample.read(3 * height * width)
                snapshot['color_image']['data'] = self.bgr_to_rgb(
                    (width, height), image_bytes)

                height, width = struct.unpack('<2I', sample.read(8))
                snapshot['depth_image'] = {'height': height, 'width': width}
                snapshot['depth_image'][
                    'data'] = sample.read(4 * height * width)

                hunger, thirst, exhaustion, happiness = struct.unpack(
                    '<4f', sample.read(16))
                snapshot['feelings'] = {'hunger': hunger,
                                        'thirst': thirst,
                                        'exhaustion': exhaustion,
                                        'happiness': happiness}
                return snapshot
            return None
