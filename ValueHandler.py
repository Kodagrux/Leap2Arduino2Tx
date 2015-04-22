import math

class ValueHandler():

	def __init__(self, maxOutput, minOutput, maxInput, minInput, nrChannels):

		self.maxOutput = maxOutput
		self.minOutput = minOutput
		self.maxInput = maxInput
		self.minInput = minInput
		self.nrChannels = nrChannels
		self.exponentials = []
		self.dualRates = []

		for x in xrange(0, self.nrChannels):
			self.exponentials.append(0)				# Default is off: 0 exponential (min)
			self.dualRates.append(1)				# Default is off: rate is 1 (max)


	def getOutput(self, channelValue, channel):
		return int(round(self.mapValue(self.calcExponential(channelValue, channel))))



	def mapValue(self, value):

		value = self.maxInput if value > self.maxInput else value
		value = self.minInput if value < self.minInput else value

		inputSpan = self.maxInput - self.minInput
		outputSpan = self.maxOutput - self.minOutput

		scaledValue = float(value - self.minInput) / float(inputSpan)

		return self.minOutput + (scaledValue * outputSpan)



	def calcExponential(self, value, channel): 				# Rangeing from 0 to 1

		if self.exponentials[channel] != 0:

			negative = False if value > 0 else True
			value = math.pow(abs(value), 1 + self.exponentials[channel])
			return value * -1 if negative else value

		else:
			return value



	def calcDualRate(self, value):

		if self.dualRate != 1:
			return value * self.dualRate
		else:
			return value



	def setExponential(self, exponential, channel):

		self.exponentials[channel] = 1 if exponential > 1 else exponential
		self.exponentials[channel] = 0 if exponential < 0 else exponential



	def setExponentials(self, exponentials):

		for x in xrange(0, self.nrChannels):
			self.setExponential(exponentials[x], x)



	def setDualRate(self, dualRate, channel):

		self.dualRates[channel] = 1 if dualRate > 1 else dualRate
		self.dualRates[channel] = 0 if dualRate < 0 else dualRate



	def setDualRates(self, dualRates):

		for x in xrange(0, self.nrChannels):
			self.setDualRate(dualRates[x], x)










