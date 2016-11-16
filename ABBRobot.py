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


	""" Traverse the blade moving upwards on the inside edge until a stop signal is sent """
	def traverseUpInsideBlade(self, currBlisk):

		pass

	""" Traverse the blade moving downwards on the inside edge until a stop signal is sent """
	def traverseDownInsideBlade(self, currBlisk):

		pass

	""" Traverse the blade moving upwards on the outside edge until a stop signal is sent """
	def traverseUpOutsideBlade(self, currBlisk):

		pass

	""" Traverse the blade moving downwards on the outside edge until a stop signal is sent """
	def traverseDownOutsideBlade(self, currBlisk):

		pass

	""" Stop the blade traversal """
	def stopBladeTraversal(self):

		pass

	""" Move the arm back away from the blisk """
	def pullArmBack(self):

		pass