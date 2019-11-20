import numpy as np

import camera
from motor import Motor
from gps import GPS
from xbee import XBee

"""
motor = Motor(left=(2, 3), right=(14, 15))
gps = GPS(time_zone=9, O_format='dd')
xbee = XBee()

current = 0
while True:
    x1, half_w, flag = camera.camera_operation(num=current)
    print(flag)
    if flag == 'ARRIVED':
        break
    else:
        if x1 is None:
            motor.move(direction='right', second=2)
        else:
            diffFromCenter = x1 - half_w
            if np.abs(diffFromCenter) > 30:
                if diffFromCenter > 0:
                    direction = 'right'
                else:
                    direction = 'left'

                motor.move2motors(direction=direction, second=1)    # cansat rotate a little,
                x2, _ = camera.camera_operation(num=-1)           # then, check how much the coordinates have changed,
                motor.to_center(x1, x2, half_w, direction)  # then, set red corn to center.

            motor.move2motors(direction='straight', second=10)    # go straight

            current += 1

print('GOAL!!')
"""

def main(motor, gps, xbee, goal_lat, goal_lon):
    # 動作開始
    xbee.justSend('Start')

    # 高度検知

    # パラシュート切り離し
    
    # gps取得
    xbee.justSend('Get first place GPS info')
    while True:
        gi0 = gps.getGPSinfo()
        if int(gi0['latitude']) == 0:
            xbee.justSend('Get GPS again')
        else:
            break
    
    # ちょっと走る
    xbee.justSend('Go straight 10 sec')
    motor.move('straight', 10)
    
    # メインループ
    xbee.justSend('Start the main loop')
    current = 0
    while True:
        # GPSデータ受信
        gi1 = gps.getGPSinfo()
        
        # 目標地点との距離と角度を計算
        d01, a01 = gps.calcDistAzim(gi0['latitude'],
                                    gi0['longitude'],
                                    gi1['latitude'],
                                    gi1['longitude'])
        xbee.justSend({'d01': d01, 'a01': a01})
        
        d1g, a1g = gps.calcDistAzim(gi1['latitude'],
                                    gi1['longitude'],
                                    goal_lat,
                                    goal_lon)
        xbee.justSend({'d1g': d1g, 'a01': a1g})
        
        # 写真を撮る
        x1, half_w, flag = camera.camera_operation(num=current)
        xbee.justSend({'x1': x1, 'flag': flag})
        if flag == 'ARRIVED':
            break

        # 障害物があるか

        # あと何ｍか
        if d1g > 10:
            angle = a1g - a01
            if angle >= 0:
                cmd = 'right'
            else:
                cmd = 'left'
            xbee.justSend({'angle': angle, 'cmd'; cmd})
            
            sec = 0.01 * angle
            motor.move(cmd, sec)
            motor.move('straight', 10)
        else:
            while x1 is None:
                motor.move('right', 3)
                x1, _, _ = camera.camera_operation(num=current)
                xbee.justSend({'x1': x1})
            motor.move('straight', 5)
            x2, _, _ = camera.camera_operation()
            motor.to_center(x1, x2, half_x)
        
        xbee.sendAndSave(count, time, flag, d1g, angle, x1)
        current += 1


if __name__ == '__main__':
    motor = Motor(left=(12, 18), right=(13, 19))
    gps = GPS(time_zone=9, O_format='dd')
    xbee = XBee()
    
    goal_lat, goal_lon = 0, 0
    
    main(motor, gps, xbee, goal_lat, goal_lon)
