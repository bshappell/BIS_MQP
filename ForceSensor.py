# ForceSensor Class
import RPi.GPIO as GPIO

class ForceSensor(object):

	def __init__(self, clkPin, doutPin, dinPin, csPin):

		# set up the pins
		self.clkPin = clkPin
		self.doutPin = doutPin
		self.dinPin = dinPin
		self.csPin = csPin

	def getForceReading(self):

		# return the current force reading
		pass

