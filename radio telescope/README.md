This is the source code to control an eight foot radio telescope.

Right now the operating system used on the raspberry pi is the Ubunutu 16.0.4 debian strech with an enabled experimental openGL driver. The driver allows stellarium to run at a decent 10 fps while without the driver stellarium only has about 2 fps and is therefore unusable.

There is an accuracy issue when converting from right ascension and declination to altitude and azimuth, then back again. The issue is that the transformations are not 100% so there is a loss of some information when the transformation is executed. It should also be noted that this results in an error of +/- .1 degrees. Since this error is significantly larger than the error due to the encoder it is considered to be the only error affecting the positioning of the telescope and therefore the total error in both directions for the telescope is +/- .1 degree each.

Furthermore, the GUI will not open until the telescope is connected to stellarium. So, if there are any errors with the GUI not opening check to make sure that stellarium is connected before anything else. This is due to the fact that the function that listens for a connection from stellarium blocks until it has a connection and is on the same thread as the GUI.

As a brief overview of how the program works there will be the option to have the telescope in manual mode where the user can move the telescope around in alt/az coordinates as he/she wishes, and there will be an automatic mode where the user selects a celestial object in stellarium and has the telescope point to that object. The basic overview for how the automatic mode works is that the telescope reads values from the encoders and based on these encoder values the program  knows the position of the telescope in the celestial sphere and checks to see if the desired object is within .1 degrees of the telescopes position in both the altitude and azimuth directions. If it is not then the telescope keeps moving until it is, if it is within .1 degrees then the telescope will stop moving in that direction. The .1 degrees comes from the fact that the error of the position of the scope is .1 degree in both directions. It therefore may be necessary to switch to manual mode to zero in on the target object.

There are some dependencies that need to be installed for the GUI to work. They are the following:

Astropy for python > 3.5

WxPython for python > 3.5

NOVAS for python > 3

Astropy and NOVAS can you can get through pip, however for wxPython you have to build it. 

To install Astropy and NOVAS first do:

Sudo apt-get install pip

then 

sudo pip3 install novas

sudo pip3 install astropy

to build wxPython follow this link

https://wiki.wxpython.org/BuildWxPythonOnRaspberryPi?fbclid=IwAR1-ENyroA_59GshzHPYHAboJNjWSDt9IsY_WWZXJ82TuHW_DurZowuOBeI
