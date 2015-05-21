import os, sys, inspect, thread, time
sys.path.insert(0, "LeapSDK")
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from Communication import Communication


class LeapListener(Leap.Listener):

	def setup(self, parent):
		self.parent = parent
		self.rawControllerData = self.parent.rawControllerData #[0,0,0,0,0,0,0,0]
		self.rawControllerData[2] = self.parent.thrustDecreaseMax
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

				if self.parent.track and hand.grab_strength < 0.5:
					self.rawControllerData[0] = (self.rawControllerData[0] + (normal.roll * -1) + self.parent.trim[0]) / 2
					self.rawControllerData[1] = (self.rawControllerData[1] + direction.pitch + self.parent.trim[1]) / 2
					self.rawControllerData[2] = (self.rawControllerData[2] + hand.palm_position[1] + self.parent.trim[2]) / 2
					self.rawControllerData[3] = (self.rawControllerData[3] + direction.yaw + self.parent.trim[3]) / 2
					
				# Toggle tracking
				if hand.grab_strength == 1 and self.lastFrameRightHandOpen:
					self.parent.track = not self.parent.track

				# Toggle sending
				if hand.pinch_strength == 1 and self.lastFramePinch and hand.grab_strength != 1:
					if not self.parent.send and self.parent.track:
						self.parent.send = True
					elif self.parent.send:
						self.parent.send = False

				# Last-frame variables 
				self.lastFrameRightHandOpen = True if hand.grab_strength != 1 else False
				self.lastFramePinch = True if hand.pinch_strength != 1 else False

		# Saftey feature so the hand resets if no righthand is visable 
		if rightHandVisable == False: 
			self.rawControllerData[0] = self.parent.defaultChannelData[0]
			self.rawControllerData[1] = self.parent.defaultChannelData[1]
			if self.parent.thustControllerMode == 1:
				self.rawControllerData[2] = (self.rawControllerData[2] - 0.7) if (self.rawControllerData[2] - 0.7) >= self.parent.thrustDecreaseMax else self.parent.thrustDecreaseMax
			else:
				self.rawControllerData[2] = self.parent.thrustNeuteralMid
			self.rawControllerData[3] = self.parent.defaultChannelData[3]
			self.parent.track = False
			self.parent.send = False


		self.lastFrame = frame

		#print self.parent.send

		#print str(self.rawControllerData)




class LeapMotion():
	
	def __init__(self, defaultChannelData, nrChannels, trim):

		self.track = False
		self.send = False
		self.thrustNeuteralMax = 250
		self.thrustNeuteralMin = 150
		self.thrustNeuteralMid = (self.thrustNeuteralMax + self.thrustNeuteralMin) / 2
		self.thrustIncreaseMax = 400
		self.thrustIncreaseMin = 251
		#self.thrustIncreaseMid = (self.thrustIncreaseMax + self.thrustIncreaseMin) / 2
		self.thrustDecreaseMax = 80
		self.thrustDecreaseMin = 149
		self.thrustSpeed = 0.06
		self.thustControllerMode = 1
		#self.thrustDecreaseMid = (self.thrustDecreaseMax + self.thrustDecreaseMin) / 2

		self.trim = trim
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

		thrust = self.calcThrust(self.rawControllerData[2], self.controllerData[2])
		self.controllerData = list(self.rawControllerData)
		self.controllerData[2] = thrust
	
		return self.controllerData



	def calcThrust(self, newThrust, currentThrust):

		if self.thustControllerMode == 1:
			#print self.mapThrust(newThrust, self.thrustIncreaseMax, self.thrustDecreaseMax, 1, -1)
			return self.mapThrust(newThrust, self.thrustIncreaseMax, self.thrustDecreaseMax, 1, -1)
		elif self.thustControllerMode == 2:
			if newThrust >= self.thrustNeuteralMax: 	# Increase Thrust

				currentThrust = currentThrust + self.mapThrust(newThrust, self.thrustIncreaseMax, self.thrustIncreaseMin, self.thrustSpeed, 0)
				currentThrust = 1 if currentThrust > 1 else currentThrust

			elif newThrust <= self.thrustNeuteralMin:	# Decrease Thrust

				currentThrust = currentThrust + self.mapThrust(newThrust, self.thrustDecreaseMin, self.thrustDecreaseMax, 0, -self.thrustSpeed)
				currentThrust = -1 if currentThrust < -1 else currentThrust
				return currentThrust
		else:
			return currentThrust



	def recalebrate(self):
		print "position hand "



	def mapThrust(self, thrust, maxInput, minInput, maxOutput, minOutput):

		thrust = maxInput if thrust > maxInput else thrust
		thrust = minInput if thrust < minInput else thrust

		inputSpan = maxInput - minInput
		outputSpan = maxOutput - minOutput

		scaledThrust = float(thrust - minInput) / float(inputSpan)

		return minOutput + (scaledThrust * outputSpan)



	def exit(self):
		self.controller.remove_listener(self.listener)


















