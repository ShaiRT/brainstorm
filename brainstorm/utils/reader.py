from pathlib import Path
import struct
import datetime as dt
import contextlib
import click
from .protocol import Hello, Config, Snapshot
from PIL import Image


class Reader:

	genders = {'m': 'male', 'f': 'female', 'o': 'other'}

	def __init__(self, path):
		self.path = path # path is a string
		with open(path, 'rb') as f:
			user_id, = struct.unpack('<Q', f.read(8))
			username_len, = struct.unpack('<I', f.read(4))
			username = struct.unpack(f'<{username_len}s', 
				f.read(username_len))[0].decode('utf-8')
			birthdate = dt.datetime.fromtimestamp(\
				struct.unpack('<I', f.read(4))[0])
			gender = struct.unpack('<c', f.read(1))[0].decode('utf-8')
			self.hello = Hello(user_id=user_id, username=username, birthdate=birthdate, gender=gender)
			self._snapshot_offset = f.tell()

	def __getattr__(self, attr):
		if attr in ['user_id', 'username', 'birthdate', 'gender']:
			return self.hello[attr]

	def __iter__(self):
		with open(self.path, 'rb') as f:
			f.seek(self._snapshot_offset, 0)
			while(True):
				snapshot = self.snapshot_from_stream(f)
				if snapshot is  None:
					break
				yield snapshot

	def __repr__(self):
		username = self.username.decode('utf-8')
		rep = f'user {self.user_id}: {username}, '
		birthday = self.birthdate.strftime('%B%e, %Y')
		rep += f'born {birthday} '
		gender = self.gender.decode('utf-8')
		rep += f'({Reader.genders[gender]})'
		return rep

	
	def bgr_to_rgb(self, image_size, image_bytes):
			image = Image.frombytes('RGB', image_size, image_bytes, 'raw', 'BGR')
			return image.tobytes()

		
	def snapshot_from_stream(self, stream):
		with contextlib.suppress(struct.error):
			ms, = struct.unpack('<Q', stream.read(8))
			datetime = dt.datetime.fromtimestamp(ms / 1000)
			s = Snapshot(datetime)
			s.translation = struct.unpack('<3d', stream.read(24))
			s.rotation = struct.unpack('<4d', stream.read(32))

			image_size = struct.unpack('<2I', stream.read(8))
			s.color_image_size = (image_size[1], image_size[0])
			image_size = image_size[0] * image_size[1]
			image_bytes = stream.read(3 * image_size)
			s.color_image = self.bgr_to_rgb(s.color_image_size, image_bytes)

			s.depth_image_size = struct.unpack('<2I', stream.read(8))
			s.depth_image = stream.read(4 * s.depth_image_size[0] * s.depth_image_size[1])
			s.feelings = struct.unpack('<4f', stream.read(16))
			return s
		return None


@click.argument('path')
def read(path):
	reader = Reader(path)
	print(reader)
	for snapshot in reader:
		print(snapshot)
