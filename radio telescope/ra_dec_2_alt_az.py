#!/usr/bin/env python
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
        """
        The purpose of this function is to get the current year, month, day and hour.
        inputs: None
        Outputs: 
        year - as an integer
        month - as an integer
        day - as an integer
        hour - as a decimal floating point number
        original author: Benjamin Vaughan
        """
        self.date = datetime.datetime.utcnow()
        date = self.date
        return date.year, date.month, date.day, date.hour + date.minute / 60.0

    def calculate(self, ra, dec):
        """
        The purpose of this function is to convert from the equatorial coordinate system to the horizontal coordinate system.
        Inputs:
        RA - right ascension of the object
        DEC - declination of the object
        Outputs:
        Azimuth - in decimal degrees
        Altitude - in decimal degrees
        Error - Error in calculation (if any)
        Original Author: Benjamin Vaughan
        """
        data = Data() #istantiates  the data class
        year, month, day, time = self.get_datetime() #obtains the current time
        utc = julian_date(year, month, day, time)
        xp, yp, ut1_utc, error = data.get_x_y_ut1_utc() #obtains xp and yp
        ut1 = utc + ut1_utc

        TT = utc + 32.184
        dt = 32.184 + self.leap_sec - ut1_utc

        zd_az, rar_decr = novas.compat.equ2hor(ut1, dt, xp, yp, self.location, ra, dec)
        alt = 90 - zd_az[0] #converts from zenith distance to altitude
        az = zd_az[1]
        return alt, az, error

    def gmst(self):
        """
        The purpose of this function is to calculate the Greenwich Mean Sidereal Time
        Inputs: None
        Outputs:
        gmst - Greenwich Mean Sidereal Time in decimal degrees
        Original Author: Benjamin Vaughan
        """
        year, month, day, hour = self.get_datetime()
        jd = julian_date(year, month, day, hour)
        t = Time(jd, format="jd", scale="utc") #creates an instance of the time class by astropy
        gmst = t.sidereal_time('mean', 'greenwich')
        gmst = gmst.value * 15 #converting gmst to degrees
        return gmst

    def lmst(self):
        """
        The purpose of this function is to calculate the local mean sidereal time
        Inputs: None
        Outputs:
        lmst - local mean sidreal time in decimal hours
        Original Author: Benjamin Vaughan
        """
        gmst = self.gmst()
        lmst = gmst + self.location.longitude
        lmst /= 15 #converting lmst to hours
        return(lmst)

    def ra_dec(self, az, alt):
        """
        The purpose of this function is to convert from the horizontal coordinate system to the equatorial coordinate system
        Inputs:
        Alt - Altitude of the object in decimal form
        Az - Azimuth of the object in decimal form
        Outputs:
        RA - right ascension of the object in decimal form
        Dec - declination of the object in decimal form
        Original Author: Benjamin Vaughan
        """

        #converting these values to radians since the m.trig functions require radians
        lat = self.location.latitude
        alt = self.degree_2_rad(alt)
        az  = self.degree_2_rad(az )
        lat = self.degree_2_rad(lat)

        #Converts azimuth to a value inbetween 0 and 360
        revs = az // 360
        c = revs * 360
        az -= c
        

        #the purpose of using try is to handle the case where there is a domain error in the calculation without the program crashing
        try:
            
            sindec = m.sin(lat)*m.sin(alt) + m.cos(lat)*m.cos(alt)*m.cos(az)
            dec = m.asin(sindec)
            sinh = -1*m.sin(az)*m.cos(alt)/m.cos(dec)
            h = m.asin(sinh)
            #cos(h) not hyperbolic cos
            cosh = (m.sin(alt) - m.sin(dec)*m.sin(lat)) / (m.cos(dec)*m.cos(lat))
            
            h = m.acos(cosh)
            #correction to give full scope of the azimuth rather than just 180 degrees
            if m.sin(az) > 0.0:
                h = 2*m.pi - h
            lha = self.rad_2_degree(h)
            lmst = self.lmst()
            #converting the local mean sidereal time to degrees
            if lmst < 0:
                lmst += 24
            lmst *= 15
            ra = lmst - lha
            
            dec = self.rad_2_degree(dec)
            return ra, dec
        except ValueError:
            ra = "error"
            dec = "error"
            return ra, dec
         
    
    def degree_2_rad(self, degrees):
        """
        The purpose of this function is to convert from degrees to radians
        Inputs:
        degrees - the degrees you want to convert
        Outputs:
        radians - the equivalent amount of radians for the degrees input
        Original Author: Benjamin Vaughan
        """
        radians = m.pi * degrees / 180
        return radians

    def rad_2_degree(self, radians):
        """
        The purpose of this function is to convert from radians to degrees
        Inputs: 
        radians - the value to be converted
        Outputs:
        degrees - the equivalent number of degrees corresponding to the input
        Original Author: Benjamin Vaughan
        """
        degrees = radians * 180 / m.pi
        return degrees

        
    
if __name__ == "__main__":

    ra_dec = Ra_Dec()
    print(ra_dec.reverse_calc(50, 220))
    print(ra_dec.gmst())
    print(ra_dec.lmst())
    print(ra_dec.ra_dec(275, -82))
