import wx
import wx.adv

class Splash(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Splash", (640,480))

        bitmap = wx.Bitmap('splash_image.jpg')
        splash = wx.adv.SplashScreen(bitmap,
                                     wx.adv.SPLASH_CENTER_ON_SCREEN |
                                     wx.adv.SPLASH_TIMEOUT,
                                     5000,
                                     self)
        splash.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = Splash()
    app.MainLoop()
