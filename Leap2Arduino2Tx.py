#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import time
from Tkinter import *

from ValueHandler import ValueHandler
from Communication import Communication
from LeapController import LeapMotion
from Application import Application

# Objects
appGUI = 0
application = 0
controller = 0
comLink = 0
valueHandler = 0

# Variables
global parameter
parameter = {
	'maxOutput' : 1100,
	'minOutput' : 0,

	'maxInput' : 1,
	'minInput' : -1,

	'defaultChannelData': [],
	'channelData': [],
	'nrChannels': 8
}

#Aditional parameters
parameter['midOutput'] = (parameter['maxOutput'] + parameter['minOutput']) / 2
parameter['midInput'] = (parameter['maxInput'] + parameter['minInput']) / 2

parameter['defaultChannelData'].append(parameter['midInput']) 		# Channel 1: Aileron
parameter['defaultChannelData'].append(parameter['midInput'])		# Channel 2: Elevator
parameter['defaultChannelData'].append(parameter['minInput']) 		# Channel 3: Thrust 
parameter['defaultChannelData'].append(parameter['midInput']) 		# Channel 4: Rudder
parameter['defaultChannelData'].append(parameter['midInput'])		# Channel 5: Gear
parameter['defaultChannelData'].append(parameter['midInput']) 		# Channel 6: Pit
parameter['defaultChannelData'].append(parameter['midInput'])		# Channel 7: Aux 1
parameter['defaultChannelData'].append(parameter['midInput'])   	# Channel 8: Aux 2
parameter['defaultChannelData'].append(parameter['midInput'])    	# Channel 9: Aux 3
parameter['defaultChannelData'].append(parameter['midInput'])    	# Channel 10: Aux 4
parameter['defaultChannelData'].append(parameter['midInput'])    	# Channel 11: Aux 5
parameter['defaultChannelData'].append(parameter['midInput'])    	# Channel 12: Aux 6


def main():
	#appGUI.mainloop()
	#comLink.connect()

	
	application.mainloop()
	quit()
	


	

	#while True:
		
		#updateChannelValues()
		#sendData()
		#time.sleep(0.05)


def initialSetup():
	global parameter 
	for x in xrange(0, parameter['nrChannels']):
		parameter['channelData'].append(parameter['defaultChannelData'][x]) 	# Reset the starting values  	

	global comLink
	comLink = Communication()

	global controller
	controller = LeapMotion(parameter['channelData'], parameter['nrChannels'])

	global valueHandler
	valueHandler = ValueHandler(parameter['maxOutput'], parameter['minOutput'], parameter['maxInput'], parameter['minInput'], parameter['nrChannels'])

	global appGUI
	appGUI = Tk()
	appGUI.geometry('800x700+100+100')

	global application
	application = Application(appGUI, controller, comLink, valueHandler, parameter)





def quit():
	comLink.disconnect()
	controller.exit()



if __name__ == "__main__":
	initialSetup()
	main()