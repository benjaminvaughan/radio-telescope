#!/usr/bin/env python3
import sys
from ra_dec_2_alt_az import *
import wx
from xp_yp_ut1_utc import Data
from ra_dec_2_alt_az import *
import traceback
from conversions import *

class Frame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size = (600, 600))
        self.panel = wx.Panel(self)

        #close button
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        #slew button
        self.btn2 = wx.Button(self.panel, -1, "Slew")
        self.Bind(wx.EVT_BUTTON, self.slew, self.btn2)

        #calculate button
        self.btn = wx.Button(self.panel, -1, "Calculate")
        self.Bind(wx.EVT_BUTTON, self.calculate, self.btn)

        #current alt
        self.txt5 = wx.TextCtrl(self.panel, -1)
        self.label5 = wx.StaticText(self.panel, label="Current Altitude")

        #current az
        self.txt6 = wx.TextCtrl(self.panel, -1)
        self.label6 = wx.StaticText(self.panel, label="Current Azimuth")
        
        #input ra
        self.txt1 = wx.TextCtrl(self.panel, -1)
        self.label1 = wx.StaticText(self.panel, label="Target Right Ascension")
        self.txt1.SetValue("0")

        #input dec
        self.txt2 = wx.TextCtrl(self.panel, -1)
        self.label2 = wx.StaticText(self.panel, label="Target Declination")
        self.txt2.SetValue("0")
        
        #creating altitude
        self.txt3 = wx.TextCtrl(self.panel, -1)
        self.label3 = wx.StaticText(self.panel, label="Target Altitude")
        self.txt3.SetValue("0")
        
        #creating azimuth
        self.txt4 = wx.TextCtrl(self.panel, -1)
        self.label4 = wx.StaticText(self.panel, label="Target Azimuth")
        self.txt4.SetValue("0")

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
        left_sizer.Add(self.label1)
        left_sizer.Add(self.txt1)
        left_sizer.Add(self.label2)
        left_sizer.Add(self.txt2)
        left_sizer.Add(self.btn)
        left_sizer.Add(self.label3)
        left_sizer.Add(self.txt3)
        left_sizer.Add(self.label4)
        left_sizer.Add(self.txt4)
        left_sizer.Add(self.btn2)

        #mid sizer
        mid_sizer.Add(self.label5)
        mid_sizer.Add(self.txt5)
        mid_sizer.Add(self.label6)
        mid_sizer.Add(self.txt6)
        
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
            alt, az = calc.calculate(float(self.txt1.GetValue()), float(self.txt2.GetValue()))
            alt_str = str(alt)
            az_str = str(az)
            self.txt3.SetValue(alt_str)
            self.txt4.SetValue(az_str)
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

if __name__ == "__main__":
    app = wx.App()
    frame = Frame(None, "Radio Telescope GUI")
    app.MainLoop()

    
