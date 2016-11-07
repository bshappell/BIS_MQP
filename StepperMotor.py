# StepperMotor Class

import RPi.GPIO as GPIO

class StepperMotor(object):

	def __init__(self, stepPin, dirPin):

		self.stepPin = stepPin
		self.dirPin = dirPin

	def increment(self):

		# increment the stepper motor once
		pass