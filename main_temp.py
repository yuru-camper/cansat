import time
import os

from guidance import camera_guidance, gps_guidance
from motor import Motor
from gps import GPS
from xbee import XBee


def main(motor, gps, xbee, giG):
    # 動作開始
    xbee.justSend('Start')
    print('start')

    angle = None
    ratio = None
    x = None
    gi0 = None

    # 高度検知
    xbee.justSend('Wait up to 40m')
    while True:
        alt = gps.getGPSinfo()['alt']
        xbee.justSend(alt)
        if alt > 40:
            break

    xbee.justSend('Wait up to 20m')
    while True:
        alt = gps.getGPSinfo()['alt']
        xbee.justSend(alt)
        if alt < 20:
            break

    time.sleep(5)

    # パラシュート切り離し
    xbee.justSend('Good-by parachute')
    motor.servo()

    # gps取得
    xbee.justSend('Get first place GPS info')
    print('get first place GPS info')
    count = 0

    xbee.justSend('Start main loop')
    print('Start main loop')
    # while True:
    while count < 60:
        xbee.justSend('count: {}'.format(count))

        gi1 = gps.getGPSinfo()
        while int(gi1['lat']) == 0:
            time.sleep(3)
            xbee.justSend('Get GPS again')
            print('get gps again')
            gi1 = gps.getGPSinfo()

        xbee.justSend('GPS is OK')
        print('gps is ok')

        d1g = gps.calcDistance(gi1, giG)
        xbee.justSend('Distance to goal: {}'.format(d1g))
        print('Distance to goal: {}'.format(d1g))

        if d1g >= 5:
            if gi0 is not None:
                angle = gps_guidance(gps, motor, xbee, gi0, gi1, giG)

            xbee.justSend('Go straight 10s')
            print('Go straight 10s')
            motor.move('straight', 10)

        else:
                x, ratio = camera_guidance(motor, xbee, count)
                if ratio >= 0.4:
                    break
        xbee.sendAndSave(count, gi1['time'], gi1['lat'], gi1['lon'], d1g, angle, x, ratio)
        gi0 = gi1
        count += 1

    xbee.sendAndSave(count, gi1['time'], gi1['lat'], gi1['lon'], d1g, angle, x, ratio)


if __name__ == '__main__':
    motor = Motor(left=(16, 12), right=(21, 20), servo_pin=23)
    gps = GPS(time_zone=9, O_format='dd')
    xbee = XBee()

    giG = {'lat': 40.1427635, 'lon': 139.987441}
    main(motor, gps, xbee, giG)

    xbee.justSend('Now Shutdown')
    os.system('sudo shutdown -h now')