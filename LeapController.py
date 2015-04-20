import os, sys, inspect, thread, time
sys.path.insert(0, "lib")
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from Communication import Communication


class LeapListener(Leap.Listener):

	def setup(self, parrent):
		self.parrent = parrent
		self.rawControllerData = self.parrent.rawControllerData #[0,0,0,0,0,0,0,0]
		self.lastFrameRightHandOpen = True


	def on_frame(self, controller):

		frame = controller.frame()
		rightHandVisable = False

		for x in xrange(0, len(frame.hands)):
			hand = frame.hands[x]
			normal = hand.palm_normal
			direction = hand.direction

			if hand.is_right: 

				rightHandVisable = True

				if self.parrent.track:
					self.rawControllerData[0] = normal.roll * -1
					self.rawControllerData[1] = direction.pitch
					self.rawControllerData[2] = hand.palm_position[1];
					self.rawControllerData[3] = direction.yaw
					
				
				if hand.grab_strength == 1 and self.lastFrameRightHandOpen: 
					self.parrent.track = not self.parrent.track


				#print self.lastFrameRightHandOpen
				self.lastFrameRightHandOpen = True if hand.grab_strength != 1 else False

		if rightHandVisable == False: # Saftey feature so the hand resets if no righthand is visable 
			self.rawControllerData[0] = self.parrent.defaultChannelData[0]
			self.rawControllerData[1] = self.parrent.defaultChannelData[1]
			self.rawControllerData[2] = self.parrent.thrustNeuteralMid
			self.rawControllerData[3] = self.parrent.defaultChannelData[3]
			self.parrent.track = False


		self.lastFrame = frame

		#print str(self.rawControllerData)




class LeapMotion():
	
	def __init__(self, defaultChannelData, nrChannels):

		self.track = False
		self.thrustNeuteralMax = 250
		self.thrustNeuteralMin = 150
		self.thrustNeuteralMid = (self.thrustNeuteralMax + self.thrustNeuteralMin) / 2
		self.thrustIncreaseMax = 400
		self.thrustIncreaseMin = 251
		#self.thrustIncreaseMid = (self.thrustIncreaseMax + self.thrustIncreaseMin) / 2
		self.thrustDecreaseMax = 80
		self.thrustDecreaseMin = 149
		#self.thrustDecreaseMid = (self.thrustDecreaseMax + self.thrustDecreaseMin) / 2

		self.defaultChannelData = list(defaultChannelData)
		self.controllerData = list(defaultChannelData)
		self.rawControllerData = list(defaultChannelData)

		self.listener = LeapListener()
		self.listener.setup(self)
		self.controller = Leap.Controller()
		self.controller.add_listener(self.listener)



	def updateControllerData(self):
		#print "INNAN " + str(self.controllerData) 
		#self.rawControllerData = self.listener.rawControllerData

		thrust = self.calcThrust(self.rawControllerData[2], self.controllerData[2]);

		
		#print str(self.rawControllerData[2])
		self.controllerData = list(self.rawControllerData)
		self.controllerData[2] = thrust;
		
		#print str(thrust) 
		
		return self.controllerData


	def calcThrust(self, newThrust, currentThrust):
		if newThrust >= self.thrustNeuteralMax: 	# Increase Thrust
			#print "more thrust " + str(newThrust)
			currentThrust = 1 if currentThrust + 0.001 > 1 else currentThrust + 0.001
		elif newThrust <= self.thrustNeuteralMin:	# Decrease Thrust
			currentThrust = -1 if currentThrust - 0.001 < -1 else currentThrust - 0.001
			#print "less thrust " + str(newThrust)
		#else:
			#print "neuteral " + str(newThrust)
		
		return currentThrust


	def recalebrate(self):
		print "position hand "



	def exit(self):
		self.controller.remove_listener(self.listener);




















