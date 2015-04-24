import sys, time, thread
from Tkinter import *


class Application(Frame):
	""" Handles UI """

	def __init__(self, parent, controller, comLink, valueHandler, parameter):
		Frame.__init__(self, parent) # Original constructor

		self.parent = parent
		self.controller = controller
		self.comLink = comLink
		self.valueHandler = valueHandler
		self.parameter = parameter

		self.setupUI()

		self.sendingThreadActive = False



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
		self.optionMenuVariable.set(comPorts[0]) # initial value
		self.optionMenu = apply(OptionMenu, (self.parent, self.optionMenuVariable) + tuple(comPorts))
		self.optionMenu.pack()


		#self.grid()
		#self.create_widgets()
		#self.reveal()
		#self.canvas.pack(fill=BOTH, expand=1)



	def create_widgets(self):
		""" create button, text and entry widget """
		self.instruction = Label(self, text = 'Status')

		""" Sets row, column and span. Sticky = west, ie left side """
		self.instruction.grid(row = 0, column = 0, columnspan = 2, sticky = W)

		# self.submit_button = Button(self, text = 'Submit', command = self.reveal)
		# self.submit_button.grid(row = 2, column = 0, sticky = W)

		#self.ball = self.canvas.create_oval(0, 20, 20, 40, outline='black', fill='gray40', tags=('ball'))

		""" Wrap = tells what value will be displayed in the box """
		'''self.text = Text(self, width = 35, height = 5, wrap = WORD)
								self.text.grid(row = 3, column = 0, columnspan = 2, sticky = W)
								self.text.insert(0.0, 'tjoho')'''

		# Start-button
		#self.quitButton = Button (self, text = 'Start', command = self.startSending)
		#self.quitButton.grid(row = 4, column = 1, sticky = W)




	def reveal(self):
		""" Display message based on password typed in """
		#0.0 is position (row, column)
		textContent = 'bara shebbel'
		self.text.delete(0.0, END)
		self.text.insert(1.0, textContent) 
		# self.text.insert(1.0, self.listener.gestureType) 
		# self.text.insert(2.0, self.listener.hand_name)
		self.after(100, self.reveal)





	def startSending(self):
		self.comLink.connect(self.optionMenuVariable.get()) 		# Connects to Arduino

		self.sendingThreadActive = True
		self.startButton.configure(text="Stop", command=self.stopSending)

		thread.start_new_thread(self.sendDataThread, (0.05,))		# Start thread
		thread.start_new_thread(self.updateUIPins, (0.05,))



	def stopSending(self):

		self.sendingThreadActive = False
		self.startButton.configure(text="Start", command=self.startSending)
		self.comLink.disconnect()




	def	sendDataThread(self, delay):

		print "Started Sending"

		while True:
			
			self.updateChannelValues()
			self.sendData()
			time.sleep(delay)

			if self.sendingThreadActive is not True:
				break

		print "Stopped Sending"




	def updateChannelValues(self):

		# Get values from controller (not the raw data but the calculated data)
		controllerData = self.controller.updateControllerData()

		# Put them in the array
		for x in xrange(0, self.parameter['nrChannels']):
			self.parameter['channelData'][x] = controllerData[x]
			


	def sendData(self):

		finalString = ""

		for x in xrange(0, self.parameter['nrChannels']):

			# Calculate the output using Value Handler
			output = self.parameter['channelOutput'][x] = self.valueHandler.getOutput(self.parameter['channelData'][x], x)
			
			# Finalize the string
			finalString = finalString + str(output) + ("," if self.parameter['nrChannels'] - 1 != x else "") 		# Value 

		# Send the data
		#print finalString
		self.comLink.send(finalString)



	


	def updateUIPins(self, delay):

		originalLeftStickCoordinates = self.canvas.coords(self.leftStick)
		originalRightStickCoordinates = self.canvas.coords(self.rightStick)

		while True:

			# Get new values for left knob
			newLeftPosX = self.calPinsOffset(self.parameter['maxOutput'] - self.parameter['channelOutput'][3], self.parameter['maxOutput'], self.parameter['minOutput'], originalLeftStickCoordinates[0], originalLeftStickCoordinates[2]-30)
			newLeftPosY = self.calPinsOffset(self.parameter['channelOutput'][2], self.parameter['maxOutput'], self.parameter['minOutput'], originalLeftStickCoordinates[1], originalLeftStickCoordinates[3]-30)

			# Get new values for right knob
			newRightPosX = self.calPinsOffset(self.parameter['maxOutput'] - self.parameter['channelOutput'][0], self.parameter['maxOutput'], self.parameter['minOutput'], originalRightStickCoordinates[0], originalRightStickCoordinates[2]-30)
			newRightPosY = self.calPinsOffset(self.parameter['maxOutput'] - self.parameter['channelOutput'][1], self.parameter['maxOutput'], self.parameter['minOutput'], originalRightStickCoordinates[1], originalRightStickCoordinates[3]-30)

			# Apply changes and move accoridngly
			self.canvas.coords(self.leftKnob, (newLeftPosX, newLeftPosY, newLeftPosX + 30, newLeftPosY + 30))
			self.canvas.coords(self.rightKnob, (newRightPosX, newRightPosY, newRightPosX + 30, newRightPosY + 30))

			self.canvas.itemconfig(self.statusText, text=str(self.parameter['channelOutput']))

			time.sleep(delay)

			# Thread 'breaker'
			if self.sendingThreadActive is not True:
				break



	def calPinsOffset(self, value, maxInput, minInput, maxOutput, minOutput):

		value = maxInput if value > maxInput else value
		value = minInput if value < minInput else value

		inputSpan = maxInput - minInput
		outputSpan = maxOutput - minOutput

		scaledValue = float(value - minInput) / float(inputSpan)

		return minOutput + (scaledValue * outputSpan)




	def quitApp(self):
		if self.sendingThreadActive:
			self.stopSending()
			time.sleep(0.05)
		self.destroy()  
		self.quit()  













