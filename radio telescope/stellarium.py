#!/usr/benv/python3

import socket
import math
from ra_dec_2_alt_az import *
import time
import struct
import select
import queue
import time

address = "127.0.0.1"
port = 10001

class Stellarium():
    def __init__(self, sock = None):
        self.ra_dec = Ra_Dec()
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.sock.bind(("", port))
        self.sock.listen(1)


    def receive_coords(self):
        """
        The purpose of this function is to receive a set of coordinates
        from stellarium and then pass those coordinates into the 
        telescope control system
        Inputs: None
        Outputs:
        alt - the altitude of the object
        az - the azimuth of the object
        Original Author: Benjamin Vaughan
        """
        inputs = [self.conn]
        outputs = []
        format = "hhiiiI"
        length = struct.calcsize(format)
        readable, writable, exceptional = select.select(inputs, outputs, inputs, .1)
        for s in readable:
            data = s.recv(length)
            if len(data) > 0:
                unpacked = struct.unpack(format, data)
                ra = float(unpacked[4]) * 90.0 / 0x40000000
                dec = float(unpacked[5]) * 180 / 0x80000000

                if ra < 0:
                    ra += 360
                rah = int(ra) // 15
                ram = int((ra- rah * 15) * 4)
                ras = (ra-rah*15 - ram / 4.0) * 240.0
                ram /= 60
                ras /= 3600
                ra = rah + ram + ras
                if dec > 270:
                    dec -= 360
                elif dec > 180:
                    dec -= 270
                elif dec > 90:
                    dec -= 180

                alt, az, error = self.ra_dec.calculate(ra, dec)
                flag = 1
                return alt, az, error, flag

        else:
            alt = 'alt'
            az = 'az'
            error = 'none'
            flag = 0
            return alt, az, error, flag

    def send(self, dec, ra):
        """
        The purpose of this function is to send the position of the telescope
        to a program called Stellarium. This program then plots the position
        of the scope relative to sky
        Inputs:
        ra - the right ascension of the telescope
        dec - the declination of the telescope
        Outputs:
        Error - error message ( if there is one )
        Original Author: Benjamin Vaughan
        """
        format = "3iIii"
        length = struct.calcsize(format)
        try:
            if ra < 0:
                ra += 360
            if dec >= 180:
                dec -= 360
            encoded_ra = ra / 90 * 0x40000000
            encoded_dec = dec / 180 *  0x80000000
        except TypeError:
            error = "failed to send data due to a value error"
            return error
        resp = struct.pack(format,
                           length,
                           0,
                           int(time.time()),
                           int(encoded_ra),
                           int(encoded_dec),
                           0)
        self.conn.send(resp)
        error = 'No error to report'

    def accept(self):
        open_sockets = []
        listening_socket = [self.sock]
        rlist, wlist, xlist = select.select(listening_socket+open_sockets, [], [])
        for i in rlist:
            if i is self.sock:
                self.conn, self.addr = self.sock.accept()
                open_sockets.append(self.conn)
                return open_sockets
