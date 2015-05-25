import sys, time, thread
from Tkinter import *


class Application(Frame):

	def __init__(self, parent, controller, comLink, valueHandler, parameter):

		# Original constructor
		Frame.__init__(self, parent) 		

		# Save parameters
		self.parent = parent
		self.controller = controller
		self.comLink = comLink
		self.valueHandler = valueHandler
		self.parameter = parameter

		# Run GUI-setup
		self.setupGUI()

		# Initial/Default loop values
		self.sendingThreadActive = False
		self.sending = False
		self.firstSend = True



	# Sets up the UI in the GUI
	def setupGUI(self):

		self.parent.title("Leap2Arduino2Tx")
		self.config(bg = '#F0F0F0')
		self.pack(fill = BOTH, expand = 1)

		# Create Canvas
		self.canvas = Canvas(self, relief = FLAT, background = "white", width = 800, height = 440)

		# Stick Containers
		self.leftStick = self.canvas.create_oval(120, 100, 320, 300, outline='gray80', fill='gray90', tags=('leftStick'))
		self.rightStick = self.canvas.create_oval(480, 100, 680, 300, outline='gray80', fill='gray90', tags=('rightStick'))
	
		# Left Knob
		self.leftKnob = self.canvas.create_oval(205, 185, 235, 215, outline='gray60', fill='gray70', tags=('leftKnob'))
		self.originalLeftKnobCoordinates = self.canvas.coords(self.leftKnob)

		# Right Knob
		self.rightKnob = self.canvas.create_oval(565, 185, 595, 215, outline='gray60', fill='gray70', tags=('rightKnob'))
		self.originalRightKnobCoordinates = self.canvas.coords(self.rightKnob)

		#Text
		self.leftStickText = self.canvas.create_text(230, 330, text="Thrust / Rudder", fill="gray50")
		self.rightStickText = self.canvas.create_text(572, 330, text="Elevator / Aileron", fill="gray50")

		# Packs canvass
		self.canvas.pack(side = TOP, anchor = NW, padx = 10, pady = 10)

		# Start-button
		self.startButton = Button(self, text = "Start", command = self.startSending, anchor = W)
		self.startButton.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
		self.startButton_window = self.canvas.create_window(400, 200, anchor=CENTER, window=self.startButton)

		# Status
		self.statusText = self.canvas.create_text(400, 380, text="", fill="gray30")

		# Nr of channels
		self.flightChannelsVariable = IntVar()
		self.flightChannels = Checkbutton(self, text = "Only use 4 channels", variable = self.flightChannelsVariable, onvalue = self.parameter['nrActiveChannels'], offvalue = self.parameter['nrChannels'], height=0, width = 21)
		self.flightChannels.select()
		self.flightChannels_window = self.canvas.create_window(315, 24, anchor=CENTER, window=self.flightChannels)

		# COM-port option menu
		comPorts = self.comLink.getPorts()
		self.optionPortMenuVariable = StringVar(self.parent)
		if len(comPorts) == 1:
			self.optionPortMenuVariable.set(comPorts[0])
		else:
			self.optionPortMenuVariable.set(comPorts[len(comPorts)-1]) 
		self.optionPortMenu = apply(OptionMenu, (self.parent, self.optionPortMenuVariable) + tuple(comPorts))

		self.port_window = self.canvas.create_window(455, 24, anchor=W, window=self.optionPortMenu)


		# Thrust mode
		thrustMode = range(1, 4)
		self.optionThrustMenuVariable = StringVar(self.parent)
		self.optionThrustMenuVariable.set(thrustMode[0])
		self.optionThrustMenu = apply(OptionMenu, (self.parent, self.optionThrustMenuVariable) + tuple(thrustMode))
		self.thrust_window = self.canvas.create_window(100, 10, anchor=NW, window=self.optionThrustMenu)
		self.thrust_window_text = self.canvas.create_text(15, 15, text="Thust mode: ", fill="black", anchor=NW)

		# Expo/DR options
		expos = []
		dualrates = []
		for x in xrange(0, 11):
			expos.append(float(x)/10)
			dualrates.append(float(x)/10)

		# Exponentials 
		self.optionExponentialMenuVariable = StringVar(self.parent)
		self.optionExponentialMenuVariable.set(expos[1])
		self.optionExponentialMenu = apply(OptionMenu, (self.parent, self.optionExponentialMenuVariable) + tuple(expos))
		self.exponentials_window = self.canvas.create_window(110, 405, anchor=NW, window=self.optionExponentialMenu)
		self.exponentials_window_text = self.canvas.create_text(15, 412, text="Exponentials: ", fill="black", anchor=NW)

		# Dual Rates
		self.optionDualRatesMenuVariable = StringVar(self.parent)
		self.optionDualRatesMenuVariable.set(dualrates[10])
		self.optionDualRatesMenu = apply(OptionMenu, (self.parent, self.optionDualRatesMenuVariable) + tuple(dualrates))
		self.dualrates_window = self.canvas.create_window(340, 405, anchor=NW, window=self.optionDualRatesMenu)
		self.dualrates_window_text = self.canvas.create_text(260, 412, text="Dual rates: ", fill="black", anchor=NW)



	# Function triggered when pressing the start-button
	def startSending(self):

		# Connects to Arduino
		self.comLink.connect(self.optionPortMenuVariable.get()) 

		# Locking options
		self.flightChannels.config(state = DISABLED)
		self.optionPortMenu.config(state = DISABLED)
		self.optionThrustMenu.config(state = DISABLED)
		self.optionDualRatesMenu.config(state = DISABLED)
		self.optionExponentialMenu.config(state = DISABLED)
		self.startButton.configure(text="Stop", command=self.stopSending)

		# Saving options
		self.nrActiveChannels = self.flightChannelsVariable.get()
		self.thrustOption = int(self.optionThrustMenuVariable.get())

		# Sets expos & dualrates
		for x in xrange(0, self.parameter['nrActiveChannels']):
			if x == 2:			# Thrust channel
				self.parameter['dualRates'][x] = 1
				self.parameter['exponentials'][x] = 0
			else:				# Channel 1, 2, 4
				self.parameter['dualRates'][x] = float(self.optionDualRatesMenuVariable.get())
				self.parameter['exponentials'][x] = float(self.optionExponentialMenuVariable.get())

		# Printing initial settings
		if self.parameter['debug']: print "Exponentials: " + str(self.parameter['exponentials'])
		if self.parameter['debug']: print "Dual Rates: " + str(self.parameter['dualRates'])
		if self.parameter['debug']: print "Thrust mode: " + self.optionThrustMenuVariable.get()
		if self.parameter['debug']: print "Number of channels used: " + str(self.flightChannelsVariable.get())

		# Applying options
		self.controller.thustControllerMode = self.thrustOption	

		# Start threads
		self.sendDefaults()
		self.sendingThreadActive = True
		thread.start_new_thread(self.sendDataThread, (self.parameter['sendingDelay'],))				# Data sender/updater	
		thread.start_new_thread(self.updateUIPins, (self.parameter['sendingDelay']+0.03,))			# UI updater (runs abit slower than the sending thread)



	# Resets the values at first send (pretty much the same as the send data thread)
	def sendDefaults(self):

		finalString = ""

		for x in xrange(0, self.parameter['nrChannels']):
			self.parameter['channelData'][x] = self.parameter['defaultChannelData'][x]
			output = self.parameter['channelOutput'][x] = self.valueHandler.getOutput(self.parameter['channelData'][x], x)

			if x == 2 and self.thrustOption == 3: 
				output = self.parameter['channelOutput'][x] = -1

			finalString = finalString + str(output) + ("," if self.parameter['nrChannels'] - 1 != x else "") 

		self.comLink.send(finalString)




	# Function triggered when pressing the stop-button
	def stopSending(self):

		# Ends thread
		self.sendingThreadActive = False
		
		# Resets parameters
		self.firstSend = True

		# Unlocking options
		self.flightChannels.config(state = NORMAL)
		self.optionPortMenu.config(state = NORMAL)
		self.optionThrustMenu.config(state = NORMAL)
		self.optionDualRatesMenu.config(state = NORMAL)
		self.optionExponentialMenu.config(state = NORMAL)
		self.startButton.configure(text="Start", command=self.startSending)



	# Main data thread
	def	sendDataThread(self, delay):

		if self.parameter['debug']: print "Started Tracking"

		# Main Loop
		while True:
			
			# Get data from Controller
			self.updateChannelValues() 		

			# Send the data to the Arduino
			self.sendData()	

			# Delay to prefent flooding the Arduino serial-port
			time.sleep(delay)				

			# Thread 'breaker'
			if self.sendingThreadActive is not True:
				break

		if self.parameter['debug']: print "Stopped Tracking"



	# Gets the data from the controller and into the Channel-data list
	def updateChannelValues(self):

		# Get values from controller (not the raw data but the calculated data)
		controllerData = self.controller.updateControllerData()

		# Sending 
		oldSend = self.sending
		self.sending = self.controller.send

		# Toggle sending
		if oldSend != self.sending:
			if self.sending:
				if self.parameter['debug']: print "Sending" 

			else:
				if self.parameter['debug']: print "Not Sending"

		# Loop through channels
		for x in xrange(0, self.nrActiveChannels):
			self.parameter['channelData'][x] = controllerData[x]


				
			


	# Function for formating the correct output and sending the data 
	def sendData(self):

		finalString = ""

		# Looping through all the channels
		for x in xrange(0, self.nrActiveChannels):

			# Calculate the output using Value Handler
			output = self.parameter['channelOutput'][x] = self.valueHandler.getOutput(self.parameter['channelData'][x], x)

			if x == 2 and self.thrustOption == 3: 
				output = self.parameter['channelOutput'][x] = -1
			
			
			# Finalize the string
			finalString = finalString + str(output) + ("," if self.nrActiveChannels - 1 != x else "") 		# Value 

			

		# Send the data 
		if self.sending:
			self.comLink.send(finalString)
			self.firstSend = False if self.firstSend else self.firstSend



	

	# Function for updating the UI Pins during flight
	def updateUIPins(self, delay):

		# Original stick containers
		originalLeftStickCoordinates = self.canvas.coords(self.leftStick)
		originalRightStickCoordinates = self.canvas.coords(self.rightStick)

		# Main Loop
		while True:

			# Get new values for left knob
			newLeftPosX = self.calPinsOffset(self.parameter['maxOutput'] + self.parameter['minOutput'] - self.parameter['channelOutput'][3], self.parameter['maxOutput'], self.parameter['minOutput'], originalLeftStickCoordinates[0] + 15, originalLeftStickCoordinates[2] - 15)
			newLeftPosY = self.calPinsOffset(self.parameter['channelOutput'][2], self.parameter['maxOutput'], self.parameter['minOutput'], originalLeftStickCoordinates[1] + 15, originalLeftStickCoordinates[3] - 15)

			# Get new values for right knob
			newRightPosX = self.calPinsOffset(self.parameter['maxOutput'] + self.parameter['minOutput'] - self.parameter['channelOutput'][0], self.parameter['maxOutput'], self.parameter['minOutput'], originalRightStickCoordinates[0] + 15, originalRightStickCoordinates[2] - 15)
			newRightPosY = self.calPinsOffset(self.parameter['maxOutput'] + self.parameter['minOutput'] - self.parameter['channelOutput'][1], self.parameter['maxOutput'], self.parameter['minOutput'], originalRightStickCoordinates[1] + 15, originalRightStickCoordinates[3] - 15)

			# Apply changes and move accoridngly
			self.canvas.coords(self.leftKnob, (newLeftPosX - 15, newLeftPosY - 15, newLeftPosX + 15, newLeftPosY + 15))
			self.canvas.coords(self.rightKnob, (newRightPosX - 15, newRightPosY - 15, newRightPosX + 15, newRightPosY + 15))

			# Prints status
			if self.parameter['debug']: self.canvas.itemconfig(self.statusText, text=str(self.parameter['channelOutput']))

			# Changing colors on Pins
			if self.sending:

				# Red
				self.canvas.itemconfig(self.leftKnob, fill='red', outline='gray30')
				self.canvas.itemconfig(self.rightKnob, fill='red', outline='gray30')
			else:

				# Original values 
				self.canvas.itemconfig(self.leftKnob, outline='gray60', fill='gray70')
				self.canvas.itemconfig(self.rightKnob, outline='gray60', fill='gray70')

			# Sleep
			time.sleep(delay)

			# Thread 'breaker'
			if self.sendingThreadActive is not True:
				break



	# Calculates the correct position of the Pins
	def calPinsOffset(self, value, maxInput, minInput, maxOutput, minOutput):

		value = maxInput if value > maxInput else value
		value = minInput if value < minInput else value

		inputSpan = maxInput - minInput
		outputSpan = maxOutput - minOutput

		scaledValue = float(value - minInput) / float(inputSpan)

		return minOutput + (scaledValue * outputSpan)



	# Exit procedure
	def quitApp(self):

		# Stop sending (if it was)
		if self.sendingThreadActive:
			self.stopSending()
			time.sleep(0.05)

		if self.parameter['debug']: print "Program Terminating"

		# GUI-stuff
		self.destroy()  
		self.quit()  










