#!/usr/bin/python3
import socket
import math
from ra_dec_2_alt_az import *
import time
import struct
import select
import queue
import time

PORT = 10001

class Stellarium():
    def __init__(self, sock = None):
        self.ra_dec = Ra_Dec()
        address = "127.0.0.1"
        port = 10004
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.sock.bind(("", PORT))
        self.sock.listen(1)
        print("Listening on %s" % PORT)

        
    def receive_send(self):
        self.conn, self.addr = self.sock.accept()
        print("connected to", self.addr)
        chunks = []
        az_tele = 0
        alt_tele = 0
        inputs = [self.conn]
        outputs = []
        while 1:
            print("Waiting")
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            print("After select")
            for s in readable:
                print("Reading")
                data = s.recv(20)
                print(len(data))
                if not data:
                    break
                if len(data) > 0:
                    print("Received %d bytes" % len(data))
                    if len(data) >= 20:
                        unpacked = struct.unpack("hhiiiI", data)
                        print(unpacked)
                        #print(unpacked[4])
                        ra = float(unpacked[4]) * 90.0 / 0x40000000 
                        dec = float(unpacked[5]) * 180.0 / float(0x80000000) 
         
                        if ra < 0:
                            ra += 360
                        rah = int(ra) // 15
                        ram = int((ra - rah * 15) * 4)
                        ras = (ra-rah*15 - ram / 4.0 ) * 240.0
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
                        target = [alt, az]
                            

                        format = "3iIii"
                        length = struct.calcsize(format)
                        az_err = az - az_tele
                        alt_err = alt - alt_tele
                        while az_err > 1 or az_err < -1:
                            az_err = az - az_tele
                            if az_err < 0:
                                az_tele -= 1
                            elif az_err > 0:
                                az_tele += 1    
                            ra_actual, dec_actual = self.ra_dec.ra_dec(az_tele, alt_tele)
                            if ra_actual == "error":
                                print('Math Domain Error')
                            else:
                                if ra_actual < 0:
                                    ra_actual += 360
                                    if dec_actual >= 180:
                                        dec_actual -= 360
                                    ra_encoded = ra_actual / 90 * 0x40000000
                                    dec_encoded = dec_actual / 180 * 0x80000000
                                    resp = struct.pack(format,
                                                       length,
                                                       0,
                                                       int(time.clock()),
                                                       int(ra_encoded),
                                                       int(dec_encoded),
                                                       0)
                                    self.conn.sendall(resp)
                                    time.sleep(.1)
                        while alt_err < -1 or alt_err > 1:
                            alt_err = alt - alt_tele
                            if alt_err < 0:
                                alt_tele -= 1
                            elif alt_err > 0:
                                alt_tele += 1
                            ra_actual, dec_actual = self.ra_dec.ra_dec(az_tele, alt_tele)
                            if ra_actual == "error":
                                print('math domain error')
                            else:
                                if ra_actual < 0:
                                    ra_actual += 360
                                if dec_actual >= 180:
                                    dec_actual -= 360
                                ra_encoded = ra_actual / 90 * 0x40000000
                                dec_encoded = dec_actual / 180 * 0x80000000
                                resp = struct.pack(format,
                                                   length,
                                                   0,
                                                   int(time.clock()),
                                                   int(ra_encoded),
                                                   int(dec_encoded),
                                                   0)
                                self.conn.sendall(resp)
                                time.sleep(.1)
                      

if __name__ == '__main__':
    stellarium = Stellarium()
    while True:
        stellarium.receive_send()
    
    
        
        
