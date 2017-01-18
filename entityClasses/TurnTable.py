# TurnTable Class

import RPi.GPIO as GPIO
from time import sleep

class TurnTable(object):

	def __init__(self, stepPin):

		self.stepPin = stepPin
		GPIO.setmode(GPIO.BCM)
		#GPIO.setwarnings(False)
		GPIO.setup(self.stepPin, GPIO.OUT)

	""" Increment the turntable one step """
	def increment(self):

		""" set the pin high and then low again """
		GPIO.output(self.stepPin, GPIO.HIGH)
		GPIO.output(self.stepPin, GPIO.LOW)

	""" Increment the turntable one blade """
	def incrementBlade(self, currStage):

		pass




if __name__=="__main__":
	
	myTurn = TurnTable(21)

	while(1):
		myTurn.increment()
		sleep(0.007)
