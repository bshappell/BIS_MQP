# ABBRobot Class
import Blisk

class ABBRobot(object):

	def __init__(self):

		pass

	""" position the arm for inspection for the current blisk """
	def positionArm(self, currBlisk):

		pass

	""" Positon the arm in the center of the current blade """
	def centerInBlade(self, currBlisk, currStage):

		pass


	""" Traverse the blade moving upwards until a stop signal is sent """
	def traverseUpBlade(self, currBlisk):

		pass

	""" Traverse the blade moving downwards until a stop signal is sent """
	def traverseDownBlade(self, currBlisk):

		pass

	""" Stop the blade traversal """
	def stopBladeTraversal(self):

		pass

	""" Move the arm back away from the blisk """
	def pullArmBack(self):

		pass