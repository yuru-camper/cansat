import serial
import micropyGPS
import time
import json
from math import cos, acos, sin, tan, atan2, sqrt, radians, degrees, pi


class GPS:

    def __init__(self, time_zone=9, O_format='dd'):
        self.gps = micropyGPS.MicropyGPS(time_zone, O_format)

    def getGPSinfo(self):
        gps = self.gps
        ser = serial.Serial('/dev/serial0', 9600, timeout=10)
        sentence = ser.readline().decode('utf-8', errors='ignore')

        for x in sentence:
            gps.update(x)

        h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
        gps_info = {'time': '%2d:%02d:%04.1f' % (h, gps.timestamp[1], gps.timestamp[2]),
                    'lat': gps.latitude[0],
                    'lon': gps.longitude[0]}

        return gps_info


    def calcDistance(self, gps_info0, gps_info1, r=6378.137):
        lat0 = radians(gps_info0['lat'])
        lon0 = radians(gps_info0['lon'])
        lat1 = radians(gps_info1['lat'])
        lon1 = radians(gps_info1['lon'])

        dist = self.distance(lat0, lon0, lat1, lon1, r) * 1e3  # 単位はm
        return dist

    def calcRotateAngle(self, gps_info0, gps_info1, gps_infoG):
        lat0 = gps_info0['lat'] - gps_info1['lat']
        lon0 = gps_info0['lon'] - gps_info1['lon']
        latG = gps_infoG['lat'] - gps_info1['lat']
        lonG = gps_infoG['lon'] - gps_info1['lon']

        cosTheta = (lat0 * latG + lon0 * lonG) / (sqrt((lat0 ** 2 + lon0 ** 2) * (latG ** 2 + lonG ** 2)) + 1e-8)
        rad_angle = acos(cosTheta)
        angle = 180 - degrees(rad_angle)

        fp = lonG * lat0 - latG * lon0  # 外積
        if fp >= 0:
            direction = 'left'
        else:
            direction = 'right'
        return angle, direction

    def distance(self, x1, y1, x2, y2, r):
        dy = y2 - y1
        val = sin(x1) * sin(x2) + cos(x1) * cos(x2) * cos(dy)
        return r * acos(val)


if __name__ == '__main__':
    gps = GPS()
    #print(gps.getGPSinfo())
    gi0 = {'lat': 40.14281213, 'lon': 139.9871054}
    giG = {'lat': 40.1427635, 'lon': 139.987441}
    print(gps.calcRotateAngle())
