#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import serial

class Communication():
	
	def __init__(self):
		self.speed = 9600
		self.ready = False
		self.port = '/dev/cu.usbmodemfa141'



	def connect(self, port):
		self.port = port
		print port
		if not hasattr(self, 'ser'):
			try:
				self.ser = serial.Serial(self.port, self.speed)
				#print str(self.ser)
			except Exception as e:
				print e.message
			finally:
				if hasattr(self, 'ser'):
					if str(self.ser.isOpen()) == 'false':
					    print 'Port now open'
					    self.ser.open()
					else:
					    print 'Port already open'
					self.ready = True
			#else:
		else:
			print "Already connected?"



	def send(self, data):
		print 'Sending message: ', data
		self.ser.write(data + '\n')



	def read(self):
		return self.ser.readline()



	def disconnect(self):
		if hasattr(self, 'ser'):
			try:
				self.ser.close();
			except Exception as e:
				print e.message

			#self.ser = None



	def getPorts(self):
		"""Lists serial ports

		:raises EnvironmentError:
		On unsupported or unknown platforms
		:returns:
		A list of available serial ports
		"""
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

