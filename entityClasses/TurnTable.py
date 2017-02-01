# TurnTable Class

import RPi.GPIO as GPIO
from time import sleep

class TurnTable(object):

	def __init__(self, stepPin):

		self.stepPin = stepPin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.stepPin, GPIO.OUT)

	""" Increment the current stage by one blade """
	def incrementBlade(currStage, blade):

		""" Iterate over each step needed to transition the curr blade """
		for step in range(currStage.getStepsForBlade(blade)):

			myTurn.increment()
			sleep(0.007)


	""" Increment the turntable one step """
	def increment(self):

		""" set the pin high and then low again """
		GPIO.output(self.stepPin, GPIO.HIGH)
		GPIO.output(self.stepPin, GPIO.LOW)


if __name__=="__main__":
	
	myTurn = TurnTable(21)

	while(1):
		myTurn.increment()
		sleep(0.002)
