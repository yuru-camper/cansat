import time
import os

import numpy as np

import camera
from motor import Motor
from xbee import XBee


def camera_guidance(motor, xbee, count):
    xbee.justSend('Take a picture')
    x1, half_width, ratio = camera.camera_operation(num=count)

    while x1 is None:
        xbee.justSend('Take a picture again')
        motor.move('right', 0.3)
        x1, _, ratio = camera.camera_operation(num=count)
    x = x1 - half_width

    xbee.justSend('Picture is OK')
    xbee.justSend('x: {}, ratio: {}'.format(x, ratio))

    if ratio < 0.4:
        xbee.justSend('Go straight little bit')
        motor.move('straight', 1)

        x2, _, ratio = camera.camera_operation()
        xbee.justSend('Red corn set to center')
        motor.to_center(x1, x2, half_width)

    return x, ratio


def gps_guidance(gps, motor, xbee, gi0, gi1, giG):
    angle, dire = gps.calcRotateAngle(gi0, gi1, giG)
    xbee.justSend('angle: {}, dire: {}'.format(angle, dire))
    print('angle: {}, dire: {}'.format(angle, dire))
    if angle > 10:
        xbee.justSend('Rotate')
        print('rotate')
        sec = 1.4 / 360 * abs(angle)
        motor.move(dire, sec)

    return angle, dire


if __name__ == '__main__':
    motor = Motor(left=(16, 12), right=(21, 20), servo_pin=23)
    xbee = XBee()
    count = 0

    while True:
        x, ratio = camera_guidance(motor, xbee, count)
        if ratio >= 0.4:
            break
        print(x, ratio)
    os.system('sudo poweroff')

