#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial

class Communication():
	

	def __init__(self):
		self.speed = 9600
		self.ready = False
		self.con = '/dev/cu.usbmodemfa141'


	def connect(self):
		if not hasattr(self, 'ser'):
			try:
				self.ser = serial.Serial(self.con, self.speed)
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
			self.ser.close();