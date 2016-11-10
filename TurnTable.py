# TurnTable Class

import RPi.GPIO as GPIO

class TurnTable(object):

	def __init__(self, stepPin, dirPin):

		self.stepPin = stepPin
		self.dirPin = dirPin

	""" Increment the turntable one step """
	def increment(self):

		# increment the stepper motor once
		pass

	""" Increment the turntable one blade """
	def incrementBlade(self, currStage):

		pass