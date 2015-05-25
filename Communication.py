#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import serial

class Communication():
	
	# Constructor
	def __init__(self, parameter):
		self.parameter = parameter
		self.speed = 9600
		self.ready = False
		self.port = '/dev/cu.usbmodemfa141'



	# Function for connection to the Ardunio
	def connect(self, port):
		self.port = port
		if not hasattr(self, 'ser'):
			try:
				self.ser = serial.Serial(self.port, self.speed)
			except Exception as e:
				if self.parameter['debug']: print e.message
			finally:
				if hasattr(self, 'ser'):
					if str(self.ser.isOpen()) == 'false':
					    if self.parameter['debug']: print 'Port now open'
					    self.ser.open()
					else:
					    if self.parameter['debug']: print 'Port already open'
					self.ready = True
		else:
			if self.parameter['debug']: print "Already connected?"



	# A simpel send-function for the Arduino
	def send(self, data):
		if self.parameter['debug']: print 'Sending message: ', data
		self.ser.write(data + '\n')



	# Reads a line
	def read(self):
		return self.ser.readline()



	# Disconnects the Arduino from the program
	def disconnect(self):
		if hasattr(self, 'ser'):
			try:
				self.ser.close();
			except Exception as e:
				if self.parameter['debug']: print e.message



	# Returns the ports available
	def getPorts(self):
		if sys.platform.startswith('win'):
			ports = ['COM' + str(i + 1) for i in range(256)]

		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		# this is to exclude your current terminal "/dev/tty"
			ports = glob.glob('/dev/tty[A-Za-z]*')

		elif sys.platform.startswith('darwin'):
			ports = glob.glob('/dev/tty.*')

		else:
			raise EnvironmentError('Unsupported platform')

		result = []
		for port in ports:
			try:
				s = serial.Serial(port)
				s.close()
				result.append(port)
			except (OSError, serial.SerialException):
				pass
		return result

