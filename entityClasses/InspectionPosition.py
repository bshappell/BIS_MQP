
""" Class to store a position along a blisk """
class InspectionPosition(object):

	def __init__(self):

		self.blisk_number = 0
		self.stage_number = 0
		self.blade_number = 0
		self.blade_side = 0
		self.small_ball_bearing = True
		self.distance = 0


	def setPos(self, blisk_number, stage_number, blade_number, blade_side, ball_bearing, distance):

		self.blisk_number = blisk_number
		self.stage_number = stage_number
		self.blade_number = blade_number
		self.blade_side = blade_side
		self.ball_bearing = ball_bearing
		self.distance = distance

	def update(self, blade_side, distance):

		self.blade_side = blade_side
		self.distance = distance
