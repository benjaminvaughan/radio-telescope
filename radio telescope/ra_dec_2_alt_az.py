
from novas.compat import *
import novas
import datetime
import math as m
from xp_yp_ut1_utc import Data
from astropy.coordinates.earth import EarthLocation
from astropy.coordinates.sky_coordinate import *
from astropy.time import Time
from astropy.coordinates.builtin_frames import AltAz
from astropy.time.core import *

class Ra_Dec():
    def __init__(self):
        self.leap_sec = 18
        self.location = OnSurface()
        self.location.latitude = 37.35
        self.location.longitude = -122
        
    def get_datetime(self):
        self.date = datetime.datetime.utcnow()
        date = self.date
        return date.year, date.month, date.day, date.hour + date.minute / 60.0

    def calculate(self, ra, dec):
        data = Data()
        year, month, day, time = self.get_datetime()
        utc = julian_date(year, month, day, time)
        xp, yp, ut1_utc, error = data.get_x_y_ut1_utc()
        ut1 = utc + ut1_utc

        TT = utc + 32.184
        dt = 32.184 + self.leap_sec - ut1_utc

        zd_az, rar_decr = novas.compat.equ2hor(ut1, dt, xp, yp, self.location, ra, dec)
        alt = 90 - zd_az[0]
        az = zd_az[1]
        return alt, az, error

    def reverse_calc(self, alt, az):
        lat = self.location.latitude
        lon = self.location.longitude
        alt = self.degree_2_rad(alt)
        az  = self.degree_2_rad(az )

        location = EarthLocation(lon = lon,
                                 lat = lat)
        year, month, day, hour = self.get_datetime()
        jd = julian_date(year, month, day, hour)

        time = Time(jd, format="jd", scale="ut1")

        altaz_frame = AltAz(obstime = time,
                            location = location,
                            temperature = 0,
                            pressure = 0.0)
        alt_az = str(alt)+ "d" + " " + str(az) + "d"
        print(alt_az)

        altaz = SkyCoord(lon, lat, unit="deg", frame=altaz_frame)

        radec_frame = "icrs"

        radec = altaz.transform_to(radec_frame)
        print(radec)

    def julian_dates(self):
        year, month, day, hour = self.get_datetime()
        jd_mn = julian_date(year, month, day - 1, 23.99)
        print(jd_mn)
        jd = jd_mn + hour / 24
        d = jd - 2451545.0
        d0 = jd_mn - 2451545.0
        print(d0)
        return d, d0

    def gmst(self):
        year, month, day, hour = self.get_datetime()
        jd = julian_date(year, month, day, hour)
        t = Time(jd, format="jd", scale="utc")
        gmst = t.sidereal_time('mean', 'greenwich')
        gmst = gmst.value * 15
        return gmst

    def lmst(self):
        gmst = self.gmst()
        lmst = gmst + self.location.longitude
        lmst /= 15
        return(lmst)

    def ra_dec(self, az, alt):
        lat = self.location.latitude
        alt = self.degree_2_rad(alt)
        az  = self.degree_2_rad(az )
        lat = self.degree_2_rad(lat)

        revs = az // 360
        c = revs * 360
        az -= c

        

        sindec = m.sin(lat)*m.sin(alt) + m.cos(lat)*m.cos(alt)*m.cos(az)
        dec = m.asin(sindec)
        sinh = -1*m.sin(az)*m.cos(alt)/m.cos(dec)
        h = m.asin(sinh)
        cosh = (m.sin(alt) - m.sin(dec)*m.sin(lat)) / (m.cos(dec)*m.cos(lat))
        h = m.acos(cosh)

        if m.sin(az) > 0.0:
            h = 2*m.pi - h
        lha = self.rad_2_degree(h)
        lmst = self.lmst()
        if lmst < 0:
            lmst += 24
        lmst *= 15
        ra = lmst - lha
        
        dec = self.rad_2_degree(dec)
        return ra, dec
    
    def degree_2_rad(self, degrees):
        radians = m.pi * degrees / 180
        return radians

    def rad_2_degree(self, radians):
        degrees = radians * 180 / m.pi
        return degrees

        
    
if __name__ == "__main__":

    ra_dec = Ra_Dec()
    print(ra_dec.reverse_calc(50, 220))
    print(ra_dec.gmst())
    print(ra_dec.lmst())
    print(ra_dec.ra_dec(275, -82))
