#!/usr/bin/env python3
import sys
from ra_dec_2_alt_az import *
import wx
from xp_yp_ut1_utc import Data
from ra_dec_2_alt_az import *
import traceback
from conversions import *
from threading import Thread
import time
from parts import *
from telescope import *
from stellarium import *
from splash import Splash

class Frame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size = (600, 600))
        self.panel = wx.Panel(self)

        #initializing class
        self.start_splash()
        self.converter = Ra_Dec()
        self.stellarium = Stellarium()
        self.stellarium.accept()
        
        #menu bar
        menubar = wx.MenuBar()
        mode = wx.Menu()
        auto_mode = wx.MenuItem(mode)
        refrac_mode = wx.MenuItem(mode)
        menubar.Append(mode, "mode")
        self.Bind(wx.EVT_MENU, self.init_auto_mode(), auto_mode)
        self.Bind(wx.EVT_MENU, self.init_refrac_mode(), refrac_mode)
        self.SetMenuBar(menubar)


    def init_refrac_mode(self):
        master_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        mid_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        master_sizer.Add(top_sizer, border=10, flag=wx.ALL|wx.EXPAND)
        top_sizer.Add(left_sizer, border=10, flag=wx.ALL|wx.EXPAND)
        top_sizer.Add(mid_sizer, border=10, flag=wx.ALL|wx.EXPAND)
        top_sizer.Add(right_sizer, border=10, flag=wx.ALL|wx.EXPAND)
        


    def init_auto_mode(self):
        
        #timer
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.get_cur_pos, self.timer)       
        self.timer.Start(100)
 
        #timer 2
        self.timer2 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.calc_diff, self.timer2)
        self.timer2.Start(100)

        #hor2equ timer
        self.hor2eq_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.cur_ra_dec, self.hor2eq_timer)
        self.hor2eq_timer.Start(100)

        #stellarium timer
        self.sttimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.send_data, self.sttimer)
        self.sttimer.Start(100)

        #stellarium timer2
        self.sttimer2 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.get_data, self.sttimer2)
        self.sttimer2.Start(500)

        #slew button
        self.btn2 = wx.Button(self.panel, -1, "Slew")
        self.Bind(wx.EVT_BUTTON, self.slew, self.btn2)

        #Emergency Stop
        self.emergency_stop = wx.Button(self.panel, -1, "Emergency Stop")
        self.Bind(wx.EVT_BUTTON, self.emergency_f, self.emergency_stop)

        #calculate button
        self.btn = wx.Button(self.panel, -1, "Calculate")
        self.Bind(wx.EVT_BUTTON, self.calculate, self.btn)

        #callibrate button
        self.calibrate_btn = wx.Button(self.panel, -1, "Calibrate")
        self.Bind(wx.EVT_BUTTON, self.calibrate, self.calibrate_btn)

        #current alt
        self.curr_alt = wx.TextCtrl(self.panel, -1)
        self.cur_alt_lab = wx.StaticText(self.panel, label="Current Altitude")

        #current az
        self.curr_az = wx.TextCtrl(self.panel, -1)
        self.cur_az_lab = wx.StaticText(self.panel, label="Current Azimuth")
        
        #input ra
        self.in_ra = wx.TextCtrl(self.panel, -1)
        self.ra_lab = wx.StaticText(self.panel, label="Target Right Ascension")
        self.in_ra.SetValue("0")

        #input dec
        self.in_dec = wx.TextCtrl(self.panel, -1)
        self.dec_lab = wx.StaticText(self.panel, label="Target Declination")
        self.in_dec.SetValue("0")
        
        #creating altitude
        self.in_alt = wx.TextCtrl(self.panel, -1)
        self.alt_lab = wx.StaticText(self.panel, label="Target Altitude")
        self.in_alt.SetValue("0")
        
        #creating azimuth
        self.in_az = wx.TextCtrl(self.panel, -1)
        self.az_lab = wx.StaticText(self.panel, label="Target Azimuth")
        self.in_az.SetValue("0")

        #Creating Right Ascension and Declination table
        self.tele_ra = wx.TextCtrl(self.panel, -1)
        self.tele_ra_lab = wx.StaticText(self.panel, label="Current Right Ascension")
        self.tele_de = wx.TextCtrl(self.panel, -1)
        self.tele_de_lab = wx.StaticText(self.panel, label="Current Declination")

        #creating error box
        self.error = wx.TextCtrl(self.panel, -1, style = wx.TE_CHARWRAP)
        self.err_label = wx.StaticText(self.panel, label="Error Messages")

        #creating ra and dec conversion table
        self.rac = wx.TextCtrl(self.panel, -1)
        self.rac_label = wx.StaticText(self.panel, label="RA (HH:MM:SS)")

        self.decc = wx.TextCtrl(self.panel, -1)
        self.decc_label = wx.StaticText(self.panel, label="DEC (DD:MM:SS)")

        self.ra_convert_btn = wx.Button(self.panel, -1, "Convert RA")
        self.Bind(wx.EVT_BUTTON, self.convert_ra, self.ra_convert_btn)
        self.dec_convert_btn = wx.Button(self.panel, -1, "Convert DEC")
        self.Bind(wx.EVT_BUTTON, self.convert_dec, self.dec_convert_btn)

        self.rad = wx.TextCtrl(self.panel, -1, style = wx.TE_READONLY)
        self.decd = wx.TextCtrl(self.panel, -1, style = wx.TE_READONLY)

        #creating the set ra and dec box
        self.set_ra = wx.TextCtrl(self.panel, -1)
        self.set_ra_label = wx.StaticText(self.panel, label="Set Altitude")
        self.set_de = wx.TextCtrl(self.panel, -1)
        self.set_de_label = wx.StaticText(self.panel, label="Set Azimuth")

        #creating difference printout
        width = 200
        self.diff_label = wx.StaticText(self.panel, label = "Difference in current and target positions")
        self.diff_label.Wrap(width)
        self.diff_az_label = wx.StaticText(self.panel, label = "Altitude")
        self.diff_alt_label = wx.StaticText(self.panel, label = "Azimuth")

        
        self.diff_az = wx.TextCtrl(self.panel, -1)
        self.diff_alt = wx.TextCtrl(self.panel, -1)
	

       
        #sizers
        master_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        mid_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        master_sizer.Add(top_sizer, border=10, flag=wx.ALL|wx.EXPAND)
        top_sizer.Add(left_sizer, border=10, flag=wx.ALL|wx.EXPAND)
        top_sizer.Add(mid_sizer, border=10, flag=wx.ALL|wx.EXPAND)
        top_sizer.Add(right_sizer, border=10, flag=wx.ALL|wx.EXPAND)

        #right sizer
        right_sizer.Add(self.rac_label)
        right_sizer.Add(self.rac)
        right_sizer.Add(self.ra_convert_btn)
        right_sizer.Add(self.rad)
        right_sizer.Add(self.decc_label)
        right_sizer.Add(self.decc)
        right_sizer.Add(self.dec_convert_btn)
        right_sizer.Add(self.decd)
        right_sizer.Add(self.set_ra_label)
        right_sizer.Add(self.set_ra)
        right_sizer.Add(self.set_de_label)
        right_sizer.Add(self.set_de)
        right_sizer.Add(self.calibrate_btn)
        right_sizer.Add(self.emergency_stop)
        
        
        #left sizer
        left_sizer.Add(self.ra_lab)
        left_sizer.Add(self.in_ra)
        left_sizer.Add(self.dec_lab)
        left_sizer.Add(self.in_dec)
        left_sizer.Add(self.btn)
        left_sizer.Add(self.alt_lab)
        left_sizer.Add(self.in_alt)
        left_sizer.Add(self.az_lab)
        left_sizer.Add(self.in_az)
        left_sizer.Add(self.btn2)

        #mid sizer
        mid_sizer.Add(self.cur_alt_lab)
        mid_sizer.Add(self.curr_alt)
        mid_sizer.Add(self.cur_az_lab)
        mid_sizer.Add(self.curr_az)
        mid_sizer.Add(self.diff_label)
        mid_sizer.Add(self.diff_az_label)
        mid_sizer.Add(self.diff_az)
        mid_sizer.Add(self.diff_alt_label)
        mid_sizer.Add(self.diff_alt)
        mid_sizer.Add(self.tele_ra_lab)
        mid_sizer.Add(self.tele_ra)
        mid_sizer.Add(self.tele_de_lab)
        mid_sizer.Add(self.tele_de)
        
        #master sizer
        master_sizer.Add(self.err_label, border=20, flag=wx.LEFT|wx.RIGHT|wx.EXPAND)
        master_sizer.Add(self.error, border=20, flag=wx.LEFT|wx.RIGHT|wx.EXPAND)
        
        self.panel.SetSizer(master_sizer)
        self.Show()

    def convert_ra(self, e):
        conversions = Conversions()
        holder = conversions.ra_2_decimal(self.rac.GetValue())
        if holder == "error":
            self.error.SetValue("Invalid Format")
        else:
            self.rad.SetValue(str(holder))
            
    def convert_dec(self, e):
        conversions = Conversions()
        holder = conversions.dec_2_decimal(self.decc.GetValue())
        if holder == "error":
            self.error.SetValue("Invalid Format")
        else:
            self.decd.SetValue(str(holder))
            
    def calculate(self, e):
        try:
            
            calc = Ra_Dec()
            alt, az, error = calc.calculate(float(self.in_ra.GetValue()), float(self.in_dec.GetValue()))
            alt_str = str(alt)
            az_str = str(az)
            self.in_alt.SetValue(alt_str)
            self.in_az.SetValue(az_str)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exc().splitlines()
            self.error.SetValue(lines[-1])

    def calc_diff(self, e):
        cur_alt = float(self.curr_alt.GetValue())
        cur_az  = float(self.curr_az.GetValue())
        tar_alt = float(self.in_alt.GetValue())
        tar_az  = float(self.in_az.GetValue())
        alt_d = cur_alt - tar_alt
        az_d = cur_az - tar_az
        self.diff_alt.SetValue(str(az_d))
        self.diff_az.SetValue(str(alt_d))

    def block_non_numbers(event):
        key_code = event.GetKeyCode()

        # Allow ASCII numerics
        if ord('0') <= key_code <= ord('9'):
            event.Skip()
            return

        # Allow decimal points
        if key_code == ord('.'):
            event.Skip()
            return
        
        # Allow tabs, for tab navigation between TextCtrls
        if key_code == ord('\t'):
            event.Skip()
            return
        
        # Block everything else
        return
        
    def OnCloseWindow(self, e):
        self.Destroy()

    def slew(self, e):
        telescope.slew(float(self.in_alt.GetValue()), float(self.in_az.GetValue()))

    def get_cur_pos(self, e):
        holder = encoder_get()
        self.curr_az.SetValue(str(holder[1]))
        self.curr_alt.SetValue(str(holder[0]))

    def cur_ra_dec(self, e):
        ra, dec = self.converter.ra_dec(float(self.curr_az.GetValue()),
                                        float(self.curr_alt.GetValue()))
        self.tele_ra.SetValue(str(ra))
        self.tele_de.SetValue(str(dec))

    def send_data(self, e):
        self.stellarium.send(float(self.tele_de.GetValue()),
                                float(self.tele_ra.GetValue()))

    def get_data(self, e):
        alt, az, error, flag = self.stellarium.receive_coords()
        if flag:
            self.in_alt.SetValue(alt)
            self.in_az.SetValue(az)
            self.error.SetValue(error)

    def calibrate(self, e):
        az = self.set_ra.GetValue()
        alt = self.set_de.GetValue()
        #telescope.azimuth_encoder.set_encoder(az)
        #telescope.altitudel_encoder.set_encoder(alt)

        #test code
        telescope.az_encoder.set_encoder(alt)
        telescope.actuator.set_encoder(az)
        self.curr_alt.SetValue(str(alt))
        self.curr_az.SetValue(str(az))

    def start_splash(self):
        splash = Splash()

    def end_splash(self):
        splash.destroy()
    
    def emergency_f(self, e):
        telescope.actuator.kill()
        telescope.az_motor.set_speed(0)

def encoder_get():
    cur_alt = telescope.actuator.get_degrees()
    cur_az = telescope.az_encoder.get_degrees()
    return cur_alt, cur_az
    

            

if __name__ == "__main__":
    app = wx.App()
    telescope = Telescope()
    frame = Frame(None, "Radio Telescope GUI")
    thread = Thread(target = encoder_get)
    thread.start()
    app.MainLoop()

    
