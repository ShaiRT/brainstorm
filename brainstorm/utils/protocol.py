import struct
import datetime as dt

class Hello:
	def __init__(self, *, user_id, username, birthdate, gender):
		self.user_id = user_id
		self.username = username
		self.birthdate = birthdate # seconds since epoch
		self.gender = gender

	def serialize(self):
		user_id = struct.pack('<Q', self.user_id)
		username_len = struct.pack('<I', len(self.username))
		username = struct.pack(f'<{len(self.username)}s', self.username.encode('utf-8'))
		birthdate = struct.pack('<I', int(self.birthdate.timestamp()))
		gender = struct.pack('<c', self.gender.encode('utf-8'))
		return user_id + username_len + username + birthdate + gender

	@classmethod
	def deserialize(cls, hello):
		user_id, username_len, hello = \
			hello[:8], hello[8:12], hello[12:]
		user_id, = struct.unpack('<Q', user_id)
		username_len, = struct.unpack('<I', username_len)
		username, hello = hello[:username_len], hello[username_len:]
		username, = struct.unpack(f'<{username_len}s', username)
		birthdate, gender = hello[:4], hello[4:]
		birthdate, = struct.unpack('<I', birthdate)
		gender, = struct.unpack('<c', gender)
		return Hello(user_id=user_id, username=username,
			birthdate=birthdate, gender=gender)

	def __getitem__(self, key):
		if key in self.__dict__:
			return self.__dict__[key]


class Config:
	def __init__(self, fields):
		self.fields = fields

	def serialize(self):
		serialized = struct.pack('<I', len(self.fields))
		for field in self.fields:
			serialized += struct.pack('<I', len(field))
			serialized += struct.pack(f'<{len(field)}s', field.encode('utf-8'))
		return serialized

	@classmethod
	def deserialize(cls, config):
		num_fields = int(struct.unpack('<I', config[:4])[0])
		config = config[4:]
		fields = []
		for i in range(num_fields):
			field_len, = struct.unpack('<I', config[:4])
			field, config = config[4:field_len + 4], config[field_len + 4:]
			field, = struct.unpack(f'<{field_len}s', field)
			fields.append(str(field))
		return Config(fields)


class Snapshot:
	def __init__(self, datetime):
		self.datetime = datetime #uint64 (milliseconds since epoch)
		self.translation = (0,0,0) #(x: double, y: double, z: double)
		self.rotation = (0,0,0,0) #(x: double, y: double, z: double, w: double)
		self.color_image_size = (0,0) #(height: uint32, width: uint32)
		self.color_image = b'' #BGR values
		self.depth_image_size = (0,0) #(height: uint32, width: uint32)
		self.depth_image = b'' #floats
		self.feelings = (0,0,0,0) #(hunger: float, thirst: float, exhaustion: float, happiness: float)

	def __repr__(self):
			date = self.datetime.strftime('%B%e, %Y')
			time = self.datetime.strftime('%H:%M:%S.%f')
			trans = '(' + ', '.join((f'{t:.1f}') for t in self.translation) + ')'
			rot = '(' + ', '.join((f'{r:.1f}') for r in self.rotation) + ')'
			rep = f'Snapshot from {date} at {time} '
			rep += f'on {trans} / {rot} with a '
			rep += f'{self.color_image_size[0]}x{self.color_image_size[1]}'
			rep += f' color image and a {self.depth_image_size[0]}x'
			rep += f'{self.depth_image_size[1]} depth image.'
			return rep

	def serialize(self):
		serialized = struct.pack('<Q', int(self.datetime.timestamp() * 1000))
		serialized += struct.pack('<3d', *self.translation)
		serialized += struct.pack('<4d', *self.rotation)
		serialized += struct.pack('<2I', *self.color_image_size)
		serialized += self.color_image
		serialized += struct.pack('<2I', *self.depth_image_size)
		serialized += self.depth_image
		serialized += struct.pack('<4f', *self.feelings)
		return serialized

	@classmethod
	def deserialize(cls, snapshot):
		ms, = struct.unpack('<Q', snapshot[:8])
		datetime = dt.datetime.fromtimestamp(ms / 1000.0)
		s = Snapshot(datetime)
		trans, rot, snapshot = \
			snapshot[8:32], snapshot[32: 64], snapshot[64:]
		s.translation = struct.unpack('<3d', trans)
		s.rotation = struct.unpack('<4d', rot)
		s.color_image_size = struct.unpack('<2I', snapshot[:8])
		s.color_image = snapshot[8: 8 + 3 * s.color_image_size[0] * s.color_image_size[1]]
		snapshot = snapshot[8 + 3 * s.color_image_size[0] * s.color_image_size[1]:]
		s.depth_image_size = struct.unpack('<2I', snapshot[:8])
		s.depth_image = snapshot[8 : 8 + 4 * s.depth_image_size[0] * s.depth_image_size[1]]
		snapshot = snapshot[8 + 4 * s.depth_image_size[0] * s.depth_image_size[1]:]
		s.feelings = struct.unpack('<4f', snapshot)
		return s
