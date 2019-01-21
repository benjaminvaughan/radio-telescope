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
#from parts import *

class Frame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size = (600, 600))
        self.panel = wx.Panel(self)

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
        #Event timer
        self.get_degree_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.get_cur_pos)

        #close button
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)


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
        print("this function needs to be written")

    def init_auto_mode(self):
        
        #timer
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.get_cur_pos, self.timer)       
        self.timer.Start(50)
 
        #slew button
        self.btn2 = wx.Button(self.panel, -1, "Slew")
        self.Bind(wx.EVT_BUTTON, self.slew, self.btn2)

        #calculate button
        self.btn = wx.Button(self.panel, -1, "Calculate")
        self.Bind(wx.EVT_BUTTON, self.calculate, self.btn)

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
        
        #master sizer
        master_sizer.Add(self.err_label, border=20, flag=wx.LEFT|wx.RIGHT|wx.EXPAND)
        master_sizer.Add(self.error, border=20, flag=wx.LEFT|wx.RIGHT|wx.EXPAND)
        
        self.panel.SetSizer(master_sizer)
        self.Show()
        self.get_degree_timer.Start(100)

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
            alt, az = calc.calculate(float(self.in_ra.GetValue()), float(self.in_dec.GetValue()))
            alt_str = str(alt)
            az_str = str(az)
            self.in_alt.SetValue(alt_str)
            self.in_az.SetValue(az_str)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exc().splitlines()
            self.error.SetValue(lines[-1])

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
        print("This function needs to be written")

    def get_cur_pos(self, e):
        holder = encoder_get()
        self.curr_az.SetValue(str(holder[1]))
        self.curr_alt.SetValue(str(holder[0]))
                             
alt_encoder = Encoder(27 , 17, "alt")
az_encoder = Encoder(24, 23, "az")


def encoder_get():
    cur_alt = alt_encoder.get_degrees()
    cur_az = az_encoder.get_degrees()
    return cur_alt, cur_az
    

            

if __name__ == "__main__":
    app = wx.App()
    alt_encoder.run_encoder()
    frame = Frame(None, "Radio Telescope GUI")
    thread = Thread(target = encoder_get)
    thread.start()
    app.MainLoop()

    
