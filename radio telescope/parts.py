import math
import pigpio
import time

class Encoder():

    def __init__(self, a_pin, b_pin, encoder_id, pi = None):
        if pi is None:
            pi = pigpio.pi()
        self.id = encoder_id
        self.pi = pi
        self.a_pin = a_pin
        self.b_pin = b_pin
        pi.set_mode(a_pin, pigpio.INPUT)
        pi.set_mode(b_pin, pigpio.INPUT)
        self.ppr = 360.0 / 600
        self.degrees = 0
        self.a_state = None
        self.position = 0

    def call_back_a(self, pin, level, tick):
        self.a_state = level

    def call_back_b(self, pin, level, tick):
        if self.a_state:
            self.position += 1
            self.direction = "clockwise"
            self.degrees = self.position * self.ppr
        else:
            self.position -= 1
            self.direction = "counter-clockwise"
            self.degrees = self.position * self.ppr
        while self.degrees < 0:
            self.degrees += 360
        while self.degrees > 360:
            self.degrees -= 360

    def get_degrees(self):
        return float(self.degrees)

    def run_encoder(self):
        self.pi.callback(self.a_pin, 2, self.call_back_a)
        self.pi.callback(self.b_pin, 1, self.call_back_b)

class Motor():
    def __init__(self, d_pin, s_pin, m1, m2, m3, pi = None):
        if pi is None:
            pi = pigpio.pi()
        self.pi = pi
        self.d_pin = d_pin
        self.s_pin = s_pin
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        pi.set_mode(d_pin, pigpio.OUTPUT)
        pi.set_mode(s_pin, pigpio.OUTPUT)
        self.mode = (m1, m2, m3)
        self.resolution = {"Full" : (0,0,0),
                           "Half" : (1,0,0),
                           "1/4"  : (0,1,0),
                           "1/8"  : (1,1,0),
                           "1/16" : (0,0,1),
                           "1/32" : (1,0,1)}
    def a32_msteps(self):
        for i in range(3):
            self.pi.write(self.mode[i], self.resolution["1/32"][i])

    def a16_msteps(self):
        for i in range(3):
            self.pi.write(self.mode[i], self.resolution["1/16"][i])

    def a8m_steps(self):
        for i in range(3):
            self.pi.write(self.mode[i], self.resolution["1/8" ][i])

    def a4_msteps(self):
        for i in range(3):
            self.pi.write(self.mode[i], self.resolution["1/4" ][i])

    def half_step(self):
        for i in range(3):
            self.pi.write(self.mode[i], self.resolution["Half"][i])

    def full_Step(self):
        for i in range(3):
            self.pi.write(self.mode[i], self.resolution["Full"][i])

    def set_speed(self, speed):
        if speed == 1:
            self.a32_msteps()
            self.set_frequency_dutycycle(128, 1000)
        elif speed == 2:
            self.a32_msteps()
            self.set_frequency_dutycycle(128, 2000)
        elif speed == 3:
            self.a16m_steps()
            self.set_frequency_dutycycle(128, 1000)
        elif speed == 4:
            self.a8_msteps()
            self.set_frequency_dutycycle(128, 1000)
        elif speed == 5:
            self.a4_msteps()
            self.set_frequency_dutycycle(128, 1000)
        elif speed == 6:
            self.half_step()
            self.set_frequency_dutycycle(128, 1000)
        elif speed == 7:
            self.full_step()
            self.set_frequency_dutycycle(128, 500)
        else:
            print("Haha")

    def set_frequency_dutycycle(self, dutycycle, frequency):
        self.pi.set_PWM_dutycycle(self.s_pin, dutycycle)
        self.pi.set_PWM_frequency(self.s_pin, frequency)

    def stop_motor(self):
        self.pi.set_PWM_dutycycle(self.s_pin, 0)

    def set_direction(self, direction):
        self.pi.write(self.d_pin, direction)

if __name__ == "__main__":
    pi = pigpio.pi()
    alt_encoder = Encoder(27, 17, "alt")
    alt_encoder.run_encoder()
    prev_degree = None
    while 1:
        if prev_degree != alt_encoder.degrees:
            alt_encoder.get_degrees()
            prev_degree1 = alt_encoder.degrees
            time.sleep(0.1)       
