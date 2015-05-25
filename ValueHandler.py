import math

class ValueHandler():

	# Init
	def __init__(self, parameter):
		self.parameter = parameter


	# Main function for getting the correct values
	def getOutput(self, channelValue, channel):
		
		return int(round(self.mapValue(self.calcDualRate(self.calcExponential(self.calcEndpoints(channelValue), channel), channel))))



	# Maps a value from one scale to another
	def mapValue(self, value):

		value = self.parameter['maxInput'] if value > self.parameter['maxInput'] else value
		value = self.parameter['minInput'] if value < self.parameter['minInput'] else value

		inputSpan = self.parameter['maxInput'] - self.parameter['minInput']
		outputSpan = self.parameter['maxOutput'] - self.parameter['minOutput']

		scaledValue = float(value - self.parameter['minInput']) / float(inputSpan)

		return self.parameter['minOutput'] + (scaledValue * outputSpan)



	# Calculating the exponential values
	def calcExponential(self, value, channel): 				# Rangeing from 0 to 1

		if self.parameter['exponentials'][channel] != 0:

			negative = False if value > 0 else True
			value = math.pow(abs(value), 1 + self.parameter['exponentials'][channel])
			return value * -1 if negative else value

		else:
			return value



	# Calculates the channel value after dual rates
	def calcDualRate(self, value, channel):

		if self.parameter['dualRates'][channel] < 1 and self.parameter['dualRates'][channel] > 0:
			return value * self.parameter['dualRates'][channel]
		else:
			return value



	# Checks max/min values
	def calcEndpoints(self, value):

		value = self.parameter['maxInput'] if value > self.parameter['maxInput'] else value
		value = self.parameter['minInput'] if value < self.parameter['minInput'] else value

		return value




