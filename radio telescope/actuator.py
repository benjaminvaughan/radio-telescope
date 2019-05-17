import pigpio
import time
import sys
import math
class Actuator():
    def __init__(self, in_a, in_b, pwm, ch_a, ch_b):
        self.pi = pi = pigpio.pi()
        self.in_a = in_a
        self.in_b = in_b
        self.pwm = pwm
        self.ch_a = ch_a
        self.ch_b = ch_b
        pi.set_mode(in_a, pigpio.OUTPUT)
        pi.set_mode(in_b, pigpio.OUTPUT)
        pi.set_mode(pwm, pigpio.OUTPUT)
        pi.set_mode(ch_a, pigpio.INPUT)
        pi.set_mode(ch_b, pigpio.INPUT)
        self.degrees = 0
        self.a_state = None
        self.ppi = 1 / 595
        self.position = 0
        self.inches = 0

    def set_encoder(self, value):
        self.degrees = value

    def callback_a(self, pin, level, tick):
        self.a_state = level

    def callback_b(self, pin, level, tick):
        if self.a_state:
            self.position += 1
            self.inches = self.position * self.ppi
        else:
            self.position -= 1
            self.inches = self.position * self.ppi
        self.degrees = math.atan(self.inches/10)

    def get_degrees(self):
        return self.degrees

    def run_encoder(self):
        self.pi.callback(self.ch_a, 2, self.callback_a)
        self.pi.callback(self.ch_b, 1, self.callback_b)

    def pull(self):
        self.pi.write(self.in_a, 1)
        self.pi.write(self.in_b, 0)

    def push(self):
        self.pi.write(self.in_a, 0)
        self.pi.write(self.in_b, 1)

    def turn_motor(self):
        dutycycle = 50
        frequency = 1000
        self.pi.set_PWM_range(self.pwm, 100)
        self.pi.set_PWM_dutycycle(self.pwm, dutycycle)
        self.pi.set_PWM_frequency(self.pwm, frequency)

    def kill(self):
        self.pi.set_PWM_frequency(self.pwm, 0)
        self.pi.set_PWM_dutycycle(self.pwm, 0)


if __name__ == "__main__":
    actuator = Actuator(27, 22, 23, 25, 24)
    if len(sys.argv) > 1:
       speed = int(sys.argv[1])

    if speed == 1:
        print('up')
        actuator.pull()
        actuator.turn_motor()
    if speed == 2:
        print('down')
        actuator.push()
        actuator.turn_motor()
    if speed == 3:
        actuator.kill()
        print('stop')
    actuator.run_encoder()
    while True:
        time.sleep(1)
