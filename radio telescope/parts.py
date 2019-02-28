#!/usr/bin/env python

import math
import pigpio
import time
import sys

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

    def set_encoder(self, value):
        self.degrees = value
        
    def call_back_a(self, pin, level, tick):
        """
        Purpose: The purpose of this function is to provide a callback to be called within pigpios callback function. It sets the value of a_state to that of the level produced by the encoder at the time of the callback
        Inputs: None
        Outputs: None
        Original Author: Benjamin Vaughan
        """
        self.a_state = level

    def call_back_b(self, pin, level, tick):
        """
        The purpose of this function is to provide a callback to be called within the pigpio callback function. It tests to see if the a_state is equal to 1 or 0 then incrememnts the position accordingly. Adittionally it converts from increments of position to degrees
        inputs: None
        Outputs: None
        """
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
        """
        Purpose: This function is used to record the current degrees determined from the encoder's ticks
        Inputs: none
        Outputs:
        self.degrees - the number of degrees the motor has turned
        Original Author: Benjamin Vaughan
        """
        return float(self.degrees)

    def run_encoder(self):
        """
        The purpose of this function is to call the callback functions defined by pigpio. This function is needed in order to run the encoders
        Inputs: None
        Outputs: None
        Original Author: Benjamin Vaughan
        """
        self.pi.callback(self.a_pin, 2, self.call_back_a)
        self.pi.callback(self.b_pin, 1, self.call_back_b)

class Motor():
    def __init__(self, d_pin, s_pin, m1, m2, m3, slp_pin, pi = None):
        if pi is None:
            pi = pigpio.pi()
        self.pi = pi
        self.d_pin = d_pin
        self.s_pin = s_pin
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.slp_pin = slp_pin
        pi.set_mode(slp_pin, pigpio.OUTPUT)
        pi.set_mode(d_pin, pigpio.OUTPUT)
        pi.set_mode(s_pin, pigpio.OUTPUT)
        self.mode = (m1, m2, m3)
        self.resolution = {"Full" : (0,0,0),
                           "Half" : (1,0,0),
                           "1/4"  : (0,1,0),
                           "1/8"  : (1,1,0),
                           "1/16" : (0,0,1),
                           "1/32" : (1,1,1)}
    def a32_msteps(self):
        """
        The purpose of this function is to set the motor to 32 microstepping mode
        inputs: none
        outputs: none
        Original Author: Benjamin Vaughan
        """
        for i in range(3):
            self.pi.write(self.mode[i], self.resolution["1/32"][i])

    def a16_msteps(self):
        """
        The purpose of this function is to set the motor to 16 microstepping mode
        inputs: none
        outputs: none
        Original Author: Benjamin Vaughan
        """
        for i in range(3):
            self.pi.write(self.mode[i], self.resolution["1/16"][i])

    def a8_msteps(self):
        """
        The purpose of this function is to set the motor to 8 microstepping mode
        inputs: none
        outputs: none
        Original Author: Benjamin Vaughan
        """
        for i in range(3):
            self.pi.write(self.mode[i], self.resolution["1/8" ][i])

    def a4_msteps(self):
        """
        The purpose of this function is to set the motor to 4 microstepping mode
        inputs: none
        outputs: none
        Original Author: Benjamin Vaughan
        """
        for i in range(3):
            self.pi.write(self.mode[i], self.resolution["1/4" ][i])

    def half_step(self):
        """
        The purpose of this function is to set the motor to 2 microstepping mode
        inputs: none
        outputs: none
        Original Author: Benjamin Vaughan
        """
        for i in range(3):
            self.pi.write(self.mode[i], self.resolution["Half"][i])

    def full_step(self):
        """
        The purpose of this function is to set the motor to full step mode
        inputs: none
        outputs: none
        Original Author: Benjamin Vaughan
        """
        for i in range(3):
            self.pi.write(self.mode[i], self.resolution["Full"][i])

    def start_motor(self):
        self.pi.write(self.slp_pin, 1)

    def set_speed(self, speed):
        """
        The purpose of this function is to check the speed input and set the motor to the matching speed
        Inputs: 
        Speed - the desired speed you want to run at range(0-7)
        outputs: None
        Original Author: Benjamin Vaughan
        """
        if speed == 0:
            self.stop_motor()
        elif speed == 1:
            self.a32_msteps()
            self.set_frequency_dutycycle(128, 800)
        elif speed == 2:
            self.a16_msteps()
            self.set_frequency_dutycycle(128, 800)
        elif speed == 3:
            self.a8_msteps()
            self.set_frequency_dutycycle(128, 800)
        elif speed == 4:
            self.a4_msteps()
            self.set_frequency_dutycycle(128, 800)
        elif speed == 5:
            self.half_step()
            self.set_frequency_dutycycle(128, 800)
        elif speed == 6:
            self.full_step()
            self.set_frequency_dutycycle(128, 800)
        elif speed == 7:
            self.full_step()
            self.set_frequency_dutycycle(128, 800)
        elif speed == 8:
            self.start_motor()
        elif speed == 9:
            self.one_step()
        else:
            print("Haha")

    def set_frequency_dutycycle(self, dutycycle, frequency):
        """
        The purpose of this function is to set the frequency and duty cycle to be sent to the motor controller from the raspberry pi
        Inputs: 
        Dutycycle - the desired dutycycle
        Frequency - the desired frequency
        Outputs: None
        Original Author: Benjamin Vaughan
        """
        self.pi.set_PWM_dutycycle(self.s_pin, dutycycle)
        self.pi.set_PWM_frequency(self.s_pin, frequency)

    def stop_motor(self):
        """
        The purpose of this function is to stop the motor from moving
        Inputs: None
        Outputs: None
        Original Author : Benjamin Vaughan
        """
        self.pi.set_PWM_dutycycle(self.s_pin, 0)
        self.pi.set_PWM_frequency(self.s_pin, 0)
        self.pi.write(self.slp_pin, 0)

    def set_direction(self, direction):
        """
        The purpose of this function is to set the direction of the motor to either clockwise or counterclockwise
        Inputs: 
        direction - (0 or 1) 1 = clockwise, 0 = counterclockwise
        Outputs: None
        Original Author : Benjamin Vaughan
        """
        self.pi.write(self.d_pin, direction)

    def one_step(self):
        self.pi.write(self.s_pin, 1)
        time.sleep(0.0206)
        self.pi.write(self.s_pin, 0)

if __name__ == "__main__":
    speed  = 7
    if len(sys.argv) > 1:
       speed = int(sys.argv[1])
    pi = pigpio.pi()
#    alt_encoder = Encoder(27, 17, "alt")
#    alt_encoder.run_encoder()
    prev_degree = None
    """
    while 1:
        if prev_degree != alt_encoder.degrees:
            alt_encoder.get_degrees()
            prev_degree1 = alt_encoder.degrees
            time.sleep(0.1)       
    """
    alt_motor = Motor(20, 21, 13, 19, 26, 16)
    alt_motor.set_direction(1)
    alt_motor.set_speed(speed)
         
