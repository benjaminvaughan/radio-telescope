import math

class Conversions():

    def __init__(self):
        pass

    def ra_2_decimal(self, ra):
        ra_list = ra.split(":")
        if len(ra_list) != 3:
            error = "error"
            return error
        if len(ra_list) == 3:
            ra_hours = float(ra_list[0])
            ra_minutes = float(ra_list[1])
            ra_seconds = float(ra_list[2])

            ra_minutes /= 60
            ra_seconds /= 3600
            ra_d = ra_hours + ra_minutes + ra_seconds
            return ra_d

    def dec_2_decimal(self, dec):
        dec_list = dec.split(":")
        if len(dec_list) != 3:
            error = "error"
            return error
        if len(dec_list) == 3:
            dec_deg = float(dec_list[0])
            dec_min = float(dec_list[1])
            dec_sec = float(dec_list[2])
            
            dec_min /= 60
            dec_sec /= 3600
            dec_d = dec_deg + dec_min + dec_sec
            return dec_d
