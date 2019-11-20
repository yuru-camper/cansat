import numpy as np
from PIL import Image
import os


def min_pooling(x):
    h, w = x.shape
    x = x.reshape((-1, 2, 2))
    x = np.min(x, axis=(1, 2))
    x = x.reshape((h // 2, w // 2))
    return x


def R_func(x):
    return 1 * (x > 0)


def G_func(x):
    return 1 * (x <= 0)


def B_func(x):
    mask0 = (x <= 0)
    mask1 = (x > 0)
    x[mask0] = 1
    x[mask1] = -1
    return x


# def capture():
#     with picamera.PiCamera() as camera:
#         camera.resolution = (640, 480)
#         time.sleep(1)
#         captured = camera.capture('captured.jpg')


def PILreshape(name):
    x = Image.open('{}.png'.format(name))
    x = x.resize(size=(256, 128))
    x.save('resize.png')


if __name__ == '__main__':
    a = np.arange(16)
    print(min_pooling(a))