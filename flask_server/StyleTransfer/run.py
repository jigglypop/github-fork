import tensorflow_hub as hub
from PIL import Image
import os
import functools
import time
import PIL.Image
import numpy as np
import tensorflow as tf
import IPython.display as display

import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime

# mpl.rcParams['figure.figsize'] = (12, 12)
# mpl.rcParams['axes.grid'] = False


def StyleTransfer(ContentPath, StylePath):
    def tensor_to_image(tensor):
        tensor = tensor*255
        tensor = np.array(tensor, dtype=np.uint8)
        if np.ndim(tensor) > 3:
            assert tensor.shape[0] == 1
            tensor = tensor[0]
        return tensor
    #   return PIL.Image.fromarray(tensor)

    def load_img(path_to_img):
        max_dim = 512
        img = tf.io.read_file(path_to_img)
        img = tf.image.decode_image(img, channels=3)
        img = tf.image.convert_image_dtype(img, tf.float32)

        shape = tf.cast(tf.shape(img)[:-1], tf.float32)
        long_dim = max(shape)
        scale = max_dim / long_dim

        new_shape = tf.cast(shape * scale, tf.int32)

        img = tf.image.resize(img, new_shape)
        img = img[tf.newaxis, :]
        return img

    def imshow(image, title=None):
        if len(image.shape) > 3:
            image = tf.squeeze(image, axis=0)
        plt.imshow(image)
        if title:
            plt.title(title)

    content_image = load_img(ContentPath)
    style_image = load_img(StylePath)
    hub_module = hub.load(
        'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/1')
    stylized_image = hub_module(tf.constant(
        content_image), tf.constant(style_image))[0]
    result = tensor_to_image(stylized_image)
    time = str(datetime.now().hour) + str(datetime.now().minute) + \
        str(datetime.now().second)
    result_name = f'result_{time}.png'
    print(result_name)
    img = Image.fromarray(result)
    UPLOAD_URL = os.getcwd() + '\\static\\styletransfer_result\\' + result_name
    img.save(UPLOAD_URL)
    return result_name
