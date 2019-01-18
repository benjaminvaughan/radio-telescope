
from novas.compat import *
import novas
import datetime
import math
from xp_yp_ut1_utc import Data

class Ra_Dec():
    def __init__(self):
        self.leap_sec = 18
        
    def get_datetime(self):
        date = datetime.datetime.utcnow()
        return date.year, date.month, date.day, date.hour + date.minute / 60.0

    def calculate(self, ra, dec):
        data = Data()
        year, month, day, time = self.get_datetime()
        utc = julian_date(year, month, day, time)
        xp, yp, ut1_utc = data.get_x_y_ut1_utc()
        ut1 = utc + ut1_utc
        location = OnSurface()
        location.latitude = 37.35
        location.longitude = -122
        TT = utc + 32.184
        dt = 32.184 + self.leap_sec - ut1_utc

        zd_az, rar_decr = novas.compat.equ2hor(ut1, dt, xp, yp, location, ra, dec)
        alt = 90 - zd_az[0]
        az = zd_az[1]
        return alt, az
    
if __name__ == "__main__":

    ra_dec = Ra_Dec()
    print(ra_dec.calculate(15, 12))
