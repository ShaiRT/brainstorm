from pathlib import Path
from PIL import Image
import json

class Parser:
	def __init__(self):
		self.fields = dict()

	def __call__(self, field):
		def decorator(f):
			self.fields[field] = f
			return f
		return decorator

	def __getattr__(self, attr):
		if attr in self.fields:
			return self.fields[attr]
		return super().__getattr__(attr)


class Context:
	def __init__(self, directory):
		self.directory = directory


parser = Parser()

@parser('translation')
def parse_translation(context, snapshot):
	trans = snapshot.translation
	trans_dict = {'x': trans[0], 'y': trans[1], 'z': trans[2]}
	context.directory.mkdir(parents=True, exist_ok=True)
	with open(context.directory / 'translation.json', 'w+') as writer:
		json.dump(trans_dict, writer)

@parser('color_image')
def parse_color_image(context, snapshot):
	context.directory.mkdir(parents=True, exist_ok=True)
	#image = Image.new('RGB', snapshot.color_image_size)
	image = Image.frombytes('RGB', snapshot.color_image_size, snapshot.color_image)
	#image.putdata(snapshot.color_image)
	image.save(context.directory / 'color_image.jpg')
