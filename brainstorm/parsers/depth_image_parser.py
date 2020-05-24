"""A snapshot depth image parser
"""
import matplotlib.image as mpl_image
import numpy as np

# from matplotlib import pyplot as plt


def parse_depth_image(snapshot):
    '''saves parsed depth image
    to the same directory of the unparsed information

    **assumes snapshot has a depth image, a user and datetime
    
    Args:
        snapshot (dict): snapshot with a depth image
    
    Returns:
        dict -- parsed depth image information
    '''
    image_info = snapshot['depth_image']
    image_size = (image_info['height'], image_info['width'])
    image_path = image_info['path'] + '.png'

    with open(image_info['path'], 'rb') as f:
        data_array = np.frombuffer(f.read(), '<f')
    pic = np.reshape(data_array, image_size)
    mpl_image.imsave(image_path, pic, cmap='plasma')
    '''
    figure, ax = plt.subplots() # fig = plt.figure()?
    ax.imshow(pic, cmap='plasma')
    figure.savefig(image_path)
    figure.clf()
    '''

    image_info['path'] = image_path
    parsed_info = dict()
    parsed_info['user'] = snapshot['user']
    parsed_info['datetime'] = snapshot['datetime']
    parsed_info['depth_image'] = image_info
    return parsed_info
