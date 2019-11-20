import time
import wiringpi
import pigpio


class Motor:
    """
    raspi  motor_driver  other
    33 --- 5
    35 --- 6
    4 ---- 7
    6 ---- 1 ----------- power_gnd
           2 ----------- motor
           4 ----------- R (>= 3k) -- 8
           8 ----------- power_v, R (>= 3k) -- 4
           10 ---------- motor
    """
    def __init__(self, left=(12, 18), right=(13, 19)):
        self.pins = [left[0], left[1], right[0], right[1]]
        self.commands = {'right': (1, 0, 1, 1),
                         'left': (1, 1, 1, 0),
                         'straight': (1, 0, 1, 0),
                         'stop': (0, 0, 0, 0)}

        # GPIO output mode to 1
        wiringpi.wiringPiSetupGpio()
        for pin in self.pins:
            wiringpi.pinMode(pin, 1)
        
        self.second = 1

    def move(self, cmd, second):
        for pin, c in zip(self.pins, self.commands[cmd]):
            wiringpi.digitalWrite(pin, c)
        time.sleep(second)

    def to_center(self, x1, x2, half_w):
        print('set red corn to center')
        dx = x1 - x2
        if dx >= 0:
            cmd = 'right'
        else:
            cmd ='left'
        second = self.second * ((half_w - dx) / dx)
        self.move(cmd, second)
        self.move('stop', 0.1)

"""
pin0 = 12
pin1 = 13
pi = pigpio.pi()
pi.set_mode(pin0, 1)
pi.set_mode(pin1, 1)

# GPIO18: 2Hz、duty比0.5
pi.hardware_PWM(pin0, 10, int(1e6))
# GPIO19: 8Hz、duty比0.1
pi.hardware_PWM(pin1, 10, int(1e5))

time.sleep(5)

pi.set_mode(pin0, pigpio.INPUT)
pi.set_mode(pin1, pigpio.INPUT)
pi.stop()
"""

if __name__ == '__main__':
    motor = Motor(left=(12, 18), right=(13, 19))
    motor.second = 2
    motor.move('straight', 10)
    motor.move('stop', 0.1)
    #motor.rotate_right()
    #motor.rotate_a_little(direction='left')
