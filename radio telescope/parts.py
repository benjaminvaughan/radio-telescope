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

    def get_degrees(self):
        print(self.degrees)
        return float(self.degrees)

    def run_encoder(self):
        self.pi.callback(self.a_pin, 2, self.call_back_a)
        self.pi.callback(self.b_pin, 1, self.call_back_b)


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
