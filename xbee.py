import serial
import time
import micropyGPS
import json

# raspi                xbee
# 1(3.3V)           ---> 1(3.3V)
# 6(GND)          ---> 10(GND)
# 8(TXD / GPIO14) ---> 3(RX)
# 10(RXD / GPIO15)---> 2(TX)

# When use GPIO: '/dev/serial0'
#          USB-serial: '/dev/ttyUSB0'
"""
ser = serial.Serial('/dev/serial0', 9600)
print(ser.portstr)

for i in range(100):
    data = "hello"
    ser.write(bytes(data, "UTF-8"))
"""
"""
time_zone = 9
O_format = 'dd'
gps = micropyGPS.MicropyGPS(time_zone, O_format)
count = 0
while True:
    gps_log = rungps()
    print(gps_log)

    data = 'count: {}, time: {}, lat: {:.5f}, lon: {:.5f}\n\r'.format(count,
                                                              gps_log['time'],
                                                              gps_log['latitude'],
                                                              gps_log['longitude'])

    ser = serial.Serial('/dev/serial0', 9600)
    ser.write(bytes(data, "UTF-8"))
    
    if count == 0:
        log = {str(count): gps_log}
    else:
        with open('log.json', 'r') as f:
            log = json.load(f)
        log[str(count)] = gps_log
    with open('log.json', 'w') as f:
        json.dump(log, f, indent='\t')
        
    time.sleep(1)
    count += 1
    
ser.close()
"""
class XBee:
    
    def __init__(self):
        self.ser = serial.Serial('/dev/serial0', 9600)

    def sendAndSave(self, count, time, flag, dist, azim, x):
        data = 'count: {}, time: {}, flag: {}, dist: {}, azim: {}, x: {}\n\r'.format(count,
                                                                                     time,
                                                                                     flag,
                                                                                     dist,
                                                                                     azim,
                                                                                     x)
        self.ser.write(bytes(data, "UTF-8"))
        
        savedir = {'time': time,
                   'flag': flag,
                   'dist': dist,
                   'azim': azim,
                   'x': x}
        if count == 0:
            log = {str(count): savedir}
        else:
            with open('log.json', 'r') as f:
                log = json.load(f)
            log[str(count)] = savedir
        with open('log.json', 'w') as f:
            json.dump(log, f, indent='\t')

    def justSend(self, dictionary):
        data = str(dictionary).strip('{').strip('}')
        self.ser.write(bytes(data, "UTF-8"))
    
    def close(self):
        self.ser.close()

if __name__ == '__main__':
    a = '{}: {}, '
    b = {'a': 1, 'b': 2}
    a *= len(b)
    print(str(b).strip('{').strip('}'))
