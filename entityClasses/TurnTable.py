# TurnTable Class
import Stage
import Blisk

import RPi.GPIO as GPIO
from time import sleep

BN_STAGE_P02 = 34
""" The Blisk IDs """
ID_BLISK_P01 = '2468M19P01'
ID_BLISK_P02 = '2468M17P02'
ID_BLISK_G02 = '2468M18G02'

""" Define the different inspection times for each blisk """
IT_BLISK_P01 = 10
IT_BLISK_P02 = 10
IT_BLISK_G02 = 20

ccw = 1
cw = 0

class TurnTable(object):

	def __init__(self, stepPin, dirPin):

		self.stepPin = stepPin
		self.dirPin = dirPin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.stepPin, GPIO.OUT)
		GPIO.setup(self.dirPin, GPIO.OUT)

	""" Increment the current stage by one blade """
	def incrementBlade(self, currStage, blade):

		""" Iterate over each step needed to transition the curr blade """
		for step in range(currStage.getStepsForBlade(blade)):

			self.increment(ccw)
			sleep(0.002)


	""" Increment the turntable one step """
	def increment(self, direction):

		""" set the pin high and then low again """
		if direction == cw:
                    GPIO.output(self.dirPin, GPIO.HIGH)
                else:
                     GPIO.output(self.dirPin, GPIO.LOW)   


		GPIO.output(self.stepPin, GPIO.HIGH)
		GPIO.output(self.stepPin, GPIO.LOW)


if __name__=="__main__":
	
	myTurn = TurnTable(23,24)
        
	stepsArray_P02 = [4667]

	""" Make the different stages Stage(numberBlades, smallBBRadius, largeBBRadius, stepsArray) """
        stage_P02 = Stage.Stage(BN_STAGE_P02, 0.122, 0.142, stepsArray_P02)

	""" The Blisks composed of the different stages Blisk(bliskID, inspectionTime, firstStage, secondStage) """
	blisk_P02 = Blisk.Blisk(ID_BLISK_P02, IT_BLISK_P02, [stage_P02])

	"""while(1):
		myTurn.increment()
		sleep(0.002)"""

	myTurn.incrementBlade(stage_P02,0)

	
