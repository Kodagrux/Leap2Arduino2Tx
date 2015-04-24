### This program is still in development and has not been tested yet (should be done by the end of May); this text will be removed when it has - 24/04/15

## Leap2Arduino2Tx
**Leap2Artudino2Tx** is makes it possible to send commands (yaw, pitch, roll, throttle) from the [Leap Motion](https://www.leapmotion.com/), via a Python-program, via an Arduino, to a R/C Transmitter. 


### Introduction
Have you ever stuck your hand out the window of your car and imagined your hand was an airplane flying thorugh the wind? No? Well, *I have*. Ever since I got into the R/C hobby a couple of years ago I've struggled with the R/C-controllers that where out there; they aren't really that user friendly and intuitive to use; you really have no idea of how you are supposed to use this controller the first time you pick it up. I set out to change this by allowing the user to control their R/C vehicle (Multirotors, Airplanes, Helicopters, etc.) using only the movement and motion of your hand (see the [Controls-section](#controls)). 

The beauties of Leap2Arduino2Tx are that it requires **no alteration** of you current R/C hardware/setup (meaning you don't need to modify your transmitter) and at the same time allows you, with the flip of a switch (the training-toggle on your controller), to **retake control** using your original transmitter. The program is also relatively **straight forward** to setup (regardless of their prior programming/computer skills) while beeing **very cheap** (depending on what you already own of course) and **platform independent** (only tested on a Mac so far).


### Disclaimer
Eventhough this project 


### Requirements
* A [Leap Motion](https://www.leapmotion.com/) (this might change in the feature, see the [Future-section](#future))
* An Arduino (preferebly one with a ATmega328 or faster) with serial-communication capabilities; [Uno R3](http://www.arduino.cc/en/Main/ArduinoBoardUno) is what I used
* The [Arduino IDE](http://www.arduino.cc/en/main/Software) (or similar; just for loading the code to the board)
* A Transmitter with a PPM-signal trainer-port (3,5 mm headphone-jack); [Turnigy 9X](http://www.hobbyking.com/hobbyking/store/__8992__Turnigy_9X_9Ch_Transmitter_w_Module_8ch_Receiver_Mode_2_v2_Firmware_.html) is what I used
* A [computer fast enough for the Leap](https://support.leapmotion.com/entries/39315178-What-are-the-system-requirements-) with [Python 2.X](https://www.python.org/downloads/) (not tested with 3.X) and [PySerial](https://pypi.python.org/pypi/pyserial) installed. You also need two USB-ports
* A [male-to-male 3,5 mm headphone-cable](https://cdn.shopify.com/s/files/1/0094/2742/products/3-55_aux_1024x1024.jpg?v=1322417365) (mono or stero; both should work)
* A way of connecting the 3,5 mm cable to the Arduino, this can be done by using a [3,5 mm chassicontact](http://www.kjell.com/image/Product_130399735477928341/full/1) (preferably mono, but stero should work) or just two [basic cables](http://www.sweetpeas.se/img/p/165-378-thickbox.jpg) with two [crocodile cables](http://ecx.images-amazon.com/images/I/41rwSISTWzL._SX355_.jpg)


### Installation
Here are the following steps for setting up and getting started. *Before* getting started you sould read the [disclaimer](#disclaimer) and [requirements](#requirements) (if you haven't already).


#### Hardware
1. Set your transmitter to training-mode, [how-to is shown here](https://www.youtube.com/watch?v=G_YuBu1E8iI), and connect the 3,5 mm cable in the back of it
2. Connect the ground of the 3,5 mm cable ([the inner part of the plug](http://www.talkandroid.com/wp-content/uploads/2010/06/pinout-audio1.png?3995d3)) to the one of the Arduino ground pins ([the bottom part in the picture](http://thietbichetao.com/wp-content/uploads/2014/03/arduino_uno_R3_pinout.jpg)) and the tip of the 3,5 mm cable plug (["Left" in this picture](http://www.talkandroid.com/wp-content/uploads/2010/06/pinout-audio1.png?3995d3), I think "Right" also works) to digital pin 2 on the Arduino ([the top/right corner in the picture](http://thietbichetao.com/wp-content/uploads/2014/03/arduino_uno_R3_pinout.jpg))
3. Connect the Arduino and the Leap to the computer via USB and move on to the [Software-section](#software) below


#### Software
Before you do this part, go through the [Hardware-section](#hardware) if you haven't already.

1. First of you need yo get Python 2.X (if you don't have it already), there are several ways of doing this and lots of tutorials online, [here is the download page](https://www.python.org/downloads/)
2. Once you have Python you need to install PySerial *for Python 2.X* (library for serial-communication). This can also be done in several ways, [here are some](http://pyserial.sourceforge.net/pyserial.html#installation)
3. To be able to manage the Arduino part you should get the [Arduino IDE](http://www.arduino.cc/en/main/Software) or similar
4. [Download the Leap2Arduino2Tx project](https://github.com/Kodagrux/Leap2Arduino2Tx/archive/master.zip), unzip the folder and navigate to the Arduino-folder located inside. You now need to get the Arduino-code (the file namned Arduino.ino) over to your Arduino board, [this is shown here](https://www.youtube.com/watch?v=kLd_JyvKV4Y)
5. Open your terminal and navigate to the Leap2Arduino2Tx-folder. Run the program by typing in `python Leap2Arduino2Tx.py` into your terminal. 


### Configuration
At the moment there isn't that much too configure, but you should select the correct COM-port (USB-port) where the Arduino is connected.


### Controls
The controls are designed to be as natural and intuative as possible, that beeing said I should mention that this concept is originally designed for quadrocopters **but** should feel very natural for both airplanes and helicopters (I doubt controlling cars makes as much sense; this might change, see the [Future-section](#future)). *Before* flying you sould read the [disclaimer](#disclaimer), if you haven't already.

* **Yaw**:
* **Pitch**:
* **Roll**:
* **Thrust**:


### Future 
* Add more channels (only 4 are currently used) and features
* Test it with more transmitters (Futuba, Spektrum, etc.)
* Add more ways of controlling (JoySticks, Nunchucks, etc.)
* Add more features in GUI (exponentials, mixing, triming, mapping etc.)
* Figure out a way to create the PPM signal from a computers headphone-jack, [like such](https://github.com/kangsterizer/Audio_PPM_Linux), or get a [USB-to-3,5 mm cable](http://www.hobbyking.com/hobbyking/store/__24348__USB_Simulator_Lead_for_Turnigy_GTX3_Transmitter_VRC_Sim_Compatible.html) and use that as an interface instead.
* Add more [controller modes](http://cdn.instructables.com/FNZ/WM1L/HINOEL7Z/FNZWM1LHINOEL7Z.LARGE.jpg) (the current is Mode 2)
* Add mode flight-modes and a camera-mode
* Package everything into one application with an icon and everything


### Known Issues
* The UI sometimes freezes (but the commands are still beeing sent)
* The program only sends channel-updates every 0.05 seconds (due to limitations in the Arduino hardware), this isn't really a problem since it's fast enough, but users should be aware.


### FAQ


### Inspirations
The following links really helped me out/inspired me with this project

* ["Manucon" by RaptorTech](https://github.com/RaptorTech/Manucon)
* [This Arduino-forum-thread](http://forum.arduino.cc/index.php?topic=8755.0)
* [This head-tracker](http://www.rcgroups.com/forums/showpost.php?p=21974105&postcount=1)
* [This article](http://www.min.at/prinz/?x=entry:entry130320-204119)
* [This YouTube-clip](https://www.youtube.com/watch?v=bBjPMjqcHAc&index=24&list=PLQeQz14wJz9wJsa7t_YXuZ6bZSYEfz1Tr)


###About this project
This project is created by, and currently only maintained by, [Arvid Bräne](http://arvidbrane.com)


###License