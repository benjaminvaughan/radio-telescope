import pigpio

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
        self.ppi = 1 / 15850
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
        print(self.inches)

    def get_degrees(self):
        return inches
        #return self.degrees

    def run_encoder(self):
        self.pi.callback(self.ch_a, 2, self.callback_a)
        self.pi.callback(self.ch_b, 1, self.callback_b)

    def push(self):
        pi.write(self.in_a, 1)
        pi.write(self.in_b, 0)

    def pull(self):
        pi.write(self.in_a, 0)
        pi.write(self.in_b, 1)

    def turn_motor(self):
        dutycycle = 20
        frequency = 1000
        pi.set_PWM_range(self.pwm, 100)
        pi.set_PWM_dutycycle(self.pwm, dutycycle)
        pi.set_PWM_frequency(self.pwm, frequency)

    def kill(self):
        pi.set_PWM_frequency(self.pwm, 0)
        pi.set_PWM_dutycycle(self.pwm, 0)


if __name__ == "__main__":
    actuator = Actuator(13, 5, 6, 19, 26)
    actuator.run_encoder()
    actuator.push()
    actuator.turn_motor()
    time.sleep(5)
    actuator.pull()
    actuator.turn_motor()
    time.sleep(5)
    actuator.kill()
    
        
