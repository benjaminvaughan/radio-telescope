from parts import *

class Telescope():

    def __init__(self):

        self.alt_encoder = Encoder(27, 17, "alt")
        self.az_encoder  = Encoder(18, 22, "az")
        self.alt_motor   = Motor(23, 24, 26, 19, 13)
        self.az_motor    = Motor(19, 26, 5, 6, 13)
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
            self.alt_motor.set_speed(1)
        elif alt_err >= 80:
            self.alt_motor.set_speed(1)
        elif alt_err >= 160:
            self.alt_motor.set_speed(1)
        elif alt_err >= 240:
            self.alt_motor.set_speed(1)

    def az_update(self, tar_az):
        az_err = self.az_dir(tar_az)
        az_err = abs(az_err)
        if az_err >= 0:
            self.az_motor.set_speed(0)
        elif az_err >= 35:
            self.az_motor.set_speed(1)
        elif az_err >= 50:
            self.az_motor.set_speed(1)
        elif az_err >= 80:
            self.az_motor.set_speed(1)
        elif az_err >= 160:
            self.az_motor.set_speed(1)
        elif az_err >= 240:
            self.az_motor.set_speed(1)

    def slew(self, tar_az, tar_alt):
        while 1:

       # cur_az = self.az_encoder.get_degrees()
       # print(cur_az)
            cur_alt = self.alt_encoder.get_degrees()
            print(cur_alt)
       # if cur_az != tar_az:
         #   self.az_update(tar_az)
            if cur_alt != tar_alt:
                 self.alt_update
    
if __name__ == "__main__":
    telescope = Telescope()
    telescope.slew(280, 100)
    
