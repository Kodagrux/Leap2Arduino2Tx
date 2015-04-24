#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
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

	'exponentials' : [0.6, 0.6, 0, 0.6, 0, 0, 0, 0],
	'controllerTrim' : [0, -0.2, 0, 0, 0, 0, 0, 0],

	'defaultChannelData': [],
	'channelData': [],
	'channelOutput': [],
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



def initialSetup():
	global parameter
	global valueHandler
	valueHandler = ValueHandler(parameter['maxOutput'], parameter['minOutput'], parameter['maxInput'], parameter['minInput'], parameter['nrChannels'])
	valueHandler.setExponentials(parameter['exponentials'])

	for x in xrange(0, parameter['nrChannels']):
		parameter['channelData'].append(parameter['defaultChannelData'][x]) 							# Reset the starting values
		parameter['channelOutput'].append(valueHandler.getOutput(parameter['channelData'][x], x)) 		# Calculating the correct output

	global comLink
	comLink = Communication()

	global controller
	controller = LeapMotion(parameter['channelData'], parameter['nrChannels'], parameter['controllerTrim'])

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
