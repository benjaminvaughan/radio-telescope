
import requests
import datetime


"""
Check if you have cached data
If so, look for today in it and return values for today
If today not found in file, or no file, get the data and save to a file
Look for today in it and return values for today
"""
class Data:
    
    def __init__(self):
        URL = 'http://maia.usno.navy.mil/ser7/mark3.out'
    
        self.req = requests.get(url = URL)
        self.now = datetime.datetime.now()

    def get_x_y_ut1_utc(self):

        """
        Purpose: get the x-coordinate and y-coordinate of the celestial intermediate pole with repect to ITRS pole in arcseconds and the utc-ut1 data from a file.
        
        Inputs:
        None
        
        Returns
        x : x-coordinate of the celestial intermediate pole
        y : y-coordinate of the celestial intermediate pole
        ut1_utc : the value of ut1-utc
        """
        
        for line in self.req.text.split('\n'):
            try:
                year = int(line[3:5])
                month = int(line[6:8])
                day = int(line[8:11])
                if year + 2000 == self.now.year and month == self.now.month and day == self.now.day:
                    elems = line.split()
                    x = float(elems[4])
                    y = float(elems[6])
                    ut1_utc = float(elems[8])
                    return x, y, ut1_utc
            except ValueError:
                pass
            
        return False
"""
if __name__ == "__main__":
    print(get_x_y_ut1_utc())
"""
