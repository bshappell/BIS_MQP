# ABBRobot Class
import Blisk

class ABBRobot(object):

	def __init__(self):

		pass

	""" position the arm for inspection for the current blisk """
	def positionArmFar(self, currBlisk):

		pass

	""" position the arm for inspection for the current blisk """
	def positionArmClose(self, currBlisk):

		pass

	""" Positon the arm in the center of the current blade """
	def inspectBlade(self, currBlisk, currStage):

		pass

	""" Move the arm back away from the blisk """
	def pullArmBack(self):

		pass

	""" Send the current force sensing measurement to the controller """
	def sendForceMeasurement(self, measurement):

		pass

	""" Handle a message received from the IRC5 controller """
	def handleMessage(self):

		pass