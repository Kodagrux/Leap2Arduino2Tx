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
		


	def setupUI(self):

		self.parent.title("Leap2Arduino2Tx")
		self.config(bg = '#F0F0F0')
		self.pack(fill = BOTH, expand = 1)

		# Create Canvas
		self.canvas = Canvas(self, relief = FLAT, background = "white", width = 800, height = 440)
		

		#self.canvas.create_rectangle(150, 10, 240, 80, outline="#f50", fill="#f50")
		self.leftStick = self.canvas.create_oval(130, 100, 330, 300, outline='gray80', fill='gray90', tags=('leftStick'))
		self.rightStick = self.canvas.create_oval(470, 100, 670, 300, outline='gray80', fill='gray90', tags=('rightStick'))
		self.leftKnob = self.canvas.create_oval(215, 185, 245, 215, outline='gray60', fill='gray70', tags=('leftKnob'))
		self.rightKnob = self.canvas.create_oval(555, 185, 585, 215, outline='gray60', fill='gray70', tags=('rightKnob'))
		self.leftStickText = self.canvas.create_text(230, 330, text="Thrust / Rudder", fill="gray50")
		self.rightStickText = self.canvas.create_text(570, 330, text="Elevator / Aileron", fill="gray50")
		#self.rightStick = self.canvas.create_oval(0, 20, 20, 40, outline='gray40', fill='gray60', tags=('ball3'))
		#self.ball.pack(side = TOP)
		self.canvas.pack(side = TOP, anchor = NW, padx = 10, pady = 10)
		# Start-button

		self.startButton = Button(self, text = "Start", command = self.start, anchor = W)
		self.startButton.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
		self.startButton_window = self.canvas.create_window(10, 10, anchor=NW, window=self.startButton)


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
		self.quitButton = Button (self, text = 'Start', command = self.start)
		self.quitButton.grid(row = 4, column = 1, sticky = W)




	def reveal(self):
		""" Display message based on password typed in """
		#0.0 is position (row, column)
		textContent = 'bara shebbel'
		self.text.delete(0.0, END)
		self.text.insert(1.0, textContent) 
		# self.text.insert(1.0, self.listener.gestureType) 
		# self.text.insert(2.0, self.listener.hand_name)
		self.after(100, self.reveal)





	def start(self):
		#self.comLink.connect() 		# Connects to Arduino

		while True:
			
			self.updateChannelValues()
			self.sendData()
			time.sleep(0.05)

			'''try:
													sys.stdin.readline()
												except KeyboardInterrupt:
													pass
												finally:
													break'''


	def updateChannelValues(self):

		controllerData = self.controller.updateControllerData()

		for x in xrange(0, self.parameter['nrChannels']):
			self.parameter['channelData'][x] = controllerData[x]
			


	def sendData(self):

		finalString = ""

		for x in xrange(0, self.parameter['nrChannels']):
			finalString = finalString + str(self.valueHandler.getOutput(self.parameter['channelData'][x])) 		# Value
			finalString = finalString + ("," if self.parameter['nrChannels'] - 1 != x else "") 					# Adding comma 


		print finalString
		#self.comLink.send(finalString)




	def quitApp(self):

		self.destroy()  #destroys root window
		self.quit()     #quits mainloop













