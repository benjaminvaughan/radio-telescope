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
        """
        The purpose of this function is to set the altitude motors direction
        Inputs: 
        tar_alt - the target altitude of the star/celestial object
        Outputs:
        alt_err - the difference between the target altitude and the actual altitude
        Original Author: Benjamin Vaughan
        """
        cur_alt = self.alt_encoder.get_degrees()
        alt_err = tar_alt - cur_alt
        if alt_err > 0:
            self.alt_motor.set_direction(1)
        else:
            self.alt_motor.set_direction(0)
        return alt_err
    
    def az_dir(self, tar_az):
        """
        The purpose of this function is to determine the direction of the azimuth motor
        Inputs:
        tar_az - target azimiuth of the celestial object
        outputs:
        az_err - the difference between tar_az and the actual azimuth of the telescope
        Original Author: Benjamin Vaughan
        """
        cur_az = self.az_encoder.get_degrees()
        az_err = tar_az - cur_az
        if az_err > 0:
            self.az_motor.set_direction(1)
        else:
            self.az_motor.set_direction(0)
        return az_err
    
    def alt_update(self, tar_alt):
        """
        The purpose of this function is to act as an update function that
        checks the distance between the target altitude and the actual altitude
        of the telescope and sets the speed of the motor accordingly
        Inputs:
        tar_alt - the target altitude of the celestial object
        outputs: None
        Original Author: Benjamin Vaughan
        """
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
        """
        The purpose of this function is to act as an update function
        that checks the distance between the target azimuth and the actual azimuth
        of the telescope and sets the speed of the motor acoordingly
        inputs: 
        tar_az - the target azimuth
        outputs: None
        Original Author: Benjamin Vaughan
        """
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
        """
        The purpose of this function is to slew the telescope to the desired
        location, it works by checking the encoder classes degrees and then 
        calling the update function for both the altitude and azimuth
        Inputs:
        tar_az - the target azimuth
        tar_alt - the target altitude
        Original Author: Benjamin Vaughan
        """
        while 1:

            cur_az = self.az_encoder.get_degrees()
            cur_alt = self.alt_encoder.get_degrees()
            if cur_az != tar_az:
                self.az_update(tar_az)
            if cur_alt != tar_alt:
                 self.alt_update
    
if __name__ == "__main__":
    telescope = Telescope()
    telescope.slew(280, 100)
    
