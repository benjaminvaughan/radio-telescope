import math
import pigpio
import time

class Encoder():

    def __init__(self, a_pin, b_pin, encoder_id, pi = None):
        if pi is None:
            pi = pigpio.pi()

            self.pi = pi
            self.a_pin = a_pin
            self.b_pin = b_pin
            pi.set_mode(a_pin, pigpio.INPUT)
            pi.set_mode(b_pin, pigpio.INPUT)
            self.ppr = 360.0 / 600

    def call_back_a(self, pin, level, tick):
        self.a_state = level

    def call_back_b(self, pin, level, tick):
        if self.a_state:
            self.position += 1
            self.direction = "clockwise"
        else:
            self.position -= 1
            self.direction = "counter-clockwise"

        self.degree = self.position * self.ppr

    def get_degrees(self):
        print("encoder", self.encoder_id, self.degree)
        return float(self.degree)

    def run_encoder(self):
        self.pi.callback(self.a_pin, 2, self.call_back_a)
        self.pi.callback(self.b_pin, 1, self.call_back_b)


if __name__ == "__main__":
    alt_encoder = Encoder(0, 2, alt)
    alt_encoder.run_encoder()

        
