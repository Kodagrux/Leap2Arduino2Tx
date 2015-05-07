import sys, time, thread
from Tkinter import *


class Application(Frame):

	def __init__(self, parent, controller, comLink, valueHandler, parameter):
		Frame.__init__(self, parent) 		# Original constructor

		self.parent = parent
		self.controller = controller
		self.comLink = comLink
		self.valueHandler = valueHandler
		self.parameter = parameter

		self.setupUI()

		self.sendingThreadActive = False
		self.sending = False



	def setupUI(self):

		self.parent.title("Leap2Arduino2Tx")
		self.config(bg = '#F0F0F0')
		self.pack(fill = BOTH, expand = 1)

		# Create Canvas
		self.canvas = Canvas(self, relief = FLAT, background = "white", width = 800, height = 440)

		# Stick Containers
		self.leftStick = self.canvas.create_oval(130, 100, 330, 300, outline='gray80', fill='gray90', tags=('leftStick'))
		self.rightStick = self.canvas.create_oval(470, 100, 670, 300, outline='gray80', fill='gray90', tags=('rightStick'))
	
		# Left Knob
		self.leftKnob = self.canvas.create_oval(215, 185, 245, 215, outline='gray60', fill='gray70', tags=('leftKnob'))
		self.originalLeftKnobCoordinates = self.canvas.coords(self.leftKnob)

		# Right Knob
		self.rightKnob = self.canvas.create_oval(555, 185, 585, 215, outline='gray60', fill='gray70', tags=('rightKnob'))
		self.originalRightKnobCoordinates = self.canvas.coords(self.rightKnob)

		#Text
		self.leftStickText = self.canvas.create_text(230, 330, text="Thrust / Rudder", fill="gray50")
		self.rightStickText = self.canvas.create_text(572, 330, text="Elevator / Aileron", fill="gray50")
		#self.rightStick = self.canvas.create_oval(0, 20, 20, 40, outline='gray40', fill='gray60', tags=('ball3'))
		#self.ball.pack(side = TOP) 
		self.canvas.pack(side = TOP, anchor = NW, padx = 10, pady = 10)

		# Start-button
		self.startButton = Button(self, text = "Start", command = self.startSending, anchor = W)
		self.startButton.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
		self.startButton_window = self.canvas.create_window(10, 10, anchor=NW, window=self.startButton)

		# Status
		self.statusText = self.canvas.create_text(400, 370, text="STATUS", fill="gray30")

		comPorts = self.comLink.getPorts()
		#print self.comLink.getPorts()
			
		# COM-port option menu
		self.optionMenuVariable = StringVar(self.parent)
		if len(comPorts) == 1:
			self.optionMenuVariable.set(comPorts[0]) # initial value
		else:
			self.optionMenuVariable.set(comPorts[len(comPorts)-1]) 
		self.optionMenu = apply(OptionMenu, (self.parent, self.optionMenuVariable) + tuple(comPorts))
		self.optionMenu.pack()



	# Function triggered when pressing the start-button
	def startSending(self):

		# Connects to Arduino
		self.comLink.connect(self.optionMenuVariable.get()) 		

		self.sendingThreadActive = True
		self.startButton.configure(text="Stop", command=self.stopSending)

		# Start threads
		thread.start_new_thread(self.sendDataThread, (0.05,))		# Data sender/updater	
		thread.start_new_thread(self.updateUIPins, (0.05,))			# UI updater



	# Function triggered when pressing the stop-button
	def stopSending(self):

		self.sendingThreadActive = False
		self.startButton.configure(text="Start", command=self.startSending)

		# Disconnect the comLink
		self.comLink.disconnect()



	# Main data thread
	def	sendDataThread(self, delay):

		print "Started Tracking"

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

		print "Stopped Tracking"




	def updateChannelValues(self):

		# Get values from controller (not the raw data but the calculated data)
		controllerData = self.controller.updateControllerData()

		# Sending 
		oldSend = self.sending
		self.sending = self.controller.send

		if oldSend != self.sending:
			print "Sending" if self.sending else "Not Sending"

		# Put them in the array
		for x in xrange(0, self.parameter['nrChannels']):
			self.parameter['channelData'][x] = controllerData[x]
			


	# Function for formating the correct output and sending the data 
	def sendData(self):

		finalString = ""

		# Looping through all the channels
		for x in xrange(0, self.parameter['nrChannels']):

			# Calculate the output using Value Handler
			output = self.parameter['channelOutput'][x] = self.valueHandler.getOutput(self.parameter['channelData'][x], x)
			
			# Finalize the string
			finalString = finalString + str(output) + ("," if self.parameter['nrChannels'] - 1 != x else "") 		# Value 

		# Send the data 
		if self.sending:
			self.comLink.send(finalString)



	

	# Function for updating the UI Pins during flight
	def updateUIPins(self, delay):

		# Original stick containers
		originalLeftStickCoordinates = self.canvas.coords(self.leftStick)
		originalRightStickCoordinates = self.canvas.coords(self.rightStick)

		# Basic correction of the max/min from stick containers
		minCorrection = 26 
		maxCorrection = 30

		# Main Loop
		while True:

			# Get new values for left knob
			newLeftPosX = self.calPinsOffset(self.parameter['maxOutput'] - self.parameter['channelOutput'][3], self.parameter['maxOutput'], self.parameter['minOutput'], originalLeftStickCoordinates[0]-minCorrection, originalLeftStickCoordinates[2]-maxCorrection)
			newLeftPosY = self.calPinsOffset(self.parameter['channelOutput'][2], self.parameter['maxOutput'], self.parameter['minOutput'], originalLeftStickCoordinates[1]-minCorrection, originalLeftStickCoordinates[3]-maxCorrection)

			# Get new values for right knob
			newRightPosX = self.calPinsOffset(self.parameter['maxOutput'] - self.parameter['channelOutput'][0], self.parameter['maxOutput'], self.parameter['minOutput'], originalRightStickCoordinates[0]-minCorrection, originalRightStickCoordinates[2]-maxCorrection)
			newRightPosY = self.calPinsOffset(self.parameter['maxOutput'] - self.parameter['channelOutput'][1], self.parameter['maxOutput'], self.parameter['minOutput'], originalRightStickCoordinates[1]-minCorrection, originalRightStickCoordinates[3]-maxCorrection)

			# Apply changes and move accoridngly
			self.canvas.coords(self.leftKnob, (newLeftPosX, newLeftPosY, newLeftPosX + 30, newLeftPosY + 30))
			self.canvas.coords(self.rightKnob, (newRightPosX, newRightPosY, newRightPosX + 30, newRightPosY + 30))

			# Prints status
			self.canvas.itemconfig(self.statusText, text=str(self.parameter['channelOutput']))

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

		# GUI-stuff
		self.destroy()  
		self.quit()  













