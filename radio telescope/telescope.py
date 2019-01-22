from parts import *

class Telescope():

    def __init__(self):
        self.alt_encoder = Encoder()
        self.az_encoder  = Encoder()
        self.alt_motor   = Motor()
        self.az_motor    = Motor()
        self.alt_encoder.run_encoder()
        self.az_encoder.run_encoder()

    def alt_dir(self, tar_alt):
        cur_alt = self.alt_encoder.get_degrees()
        alt_err = tar_alt - cur_alt
        if alt_err > 0:
            self.alt_motor.set_direction(1)
        else:
            self.alt_motor.set_direction(0)
        return alt_err
    
    def az_dir(self, tar_az):
        cur_az = self.az_encoder.get_degrees()
        az_err = tar_az - cur_az
        if az_err > 0:
            self.az_motor.set_direction(1)
        else:
            self.az_motor.set_direction(0)
        return az_err
    
    def alt_update(self, tar_alt):
        alt_err = self.alt_dir(tar_alt)
        alt_err = abs(alt_err)
        if alt_err >= 0:
            self.alt_motor.stop_motor()
        elif alt_err >= 35:
            self.alt_motor.set_speed(1)
        elif alt_err >= 50:
            self.alt_motor.set_speed(2)
        elif alt_err >= 80:
            self.alt_motor.set_speed(3)
        elif alt_err >= 160:
            self.alt_motor.set_speed(4)
        elif alt_err >= 240:
            self.alt_motor.set_speed(5)
        elif alt_err >= 300:
            self.alt_motor.set_speed(6)
        elif alt_err >= 360:
            self.alt_motor.set_speed(7)

    def az_update(self, tar_az):
        az_err = self.az_dir(tar_az)
        az_err = abs(az_err)
        if az_err >= 0:
            self.az_motor.stop_motor()
        elif az_err >= 35:
            self.az_motor.set_speed(1)
        elif az_err >= 50:
            self.az_motor.set_speed(2)
        elif az_err >= 80:
            self.az_motor.set_speed(3)
        elif az_err >= 160:
            self.az_motor.set_speed(4)
        elif az_err >= 240:
            self.az_motor.set_speed(5)
        elif az_err >= 300:
            self.az_motor.set_speed(6)
        elif az_err >= 360:
            self.az_motor.set_speed(7)

    def slew(self, tar_az, tar_alt):
        cur_az = az_encoder.get_degrees()
        cur_alt = alt_encoder.get_degrees()
        if cur_az != tar_az:
            self.az_update(tar_az)
        if cur_alt 1= tar_alt:
            self.alt_update
    
if __name__ == "__main__":
    telescope = Telescope()
    telescope.slew(280, 100)
    
