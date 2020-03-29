import numpy as np
from matplotlib import pyplot as plt


def parse_depth_image(snapshot):
    image_info = snapshot['depth_image']
    image_size = (image_info['height'], image_info['width'])
    image_path = image_info['path'] + '.png'

    with open(image_info['path'], 'rb') as f:
        data_array = np.frombuffer(f.read(), '<f')
    pic = np.reshape(data_array, image_size)
    figure, ax = plt.subplots()
    ax.imshow(pic, cmap='plasma')
    figure.savefig(image_path)
    figure.clf()

    image_info['path'] = image_path
    parsed_info = dict()
    parsed_info['user'] = snapshot['user']
    parsed_info['datetime'] = snapshot['datetime']
    parsed_info['depth_image'] = image_info
    return parsed_info
