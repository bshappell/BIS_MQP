
""" Class to store a position along a blisk """
class InspectionPosition(object):

	def __init__(self):

		self.blisk_number = 0
		self.stage_number = 0
		self.blade_number = 0
		self.blade_side = 0
		self.ball_bearing = 0
		self.distance = 0
		self.blisk_string = ""

	def setPos(self, blisk_number, stage_number, blade_number, blade_side, ball_bearing, distance):

		""" Set the blisk number and string """
		if blisk_number == 0:
			self.blisk_string = "P01"
			self.blisk_number = blisk_number
		elif blisk_number == 1:
			self.blisk_string = "P02"
			self.blisk_number = blisk_number
		elif blisk_number == 2:
			self.blisk_string = "G02"
			self.blisk_number = blisk_number
		else: 
			self.my_print("ERROR INCORRECT BLISK NUMBER RECEIVED IN PREP INSP CLOSE")

		""" Check and set the stage number """
		if ((stage_number == 1) and (self.blisk_number == 2)):
			self.stage_number = 1
		else:
			self.stage_number = 0

		self.blade_number = blade_number
		self.blade_side = blade_side
		self.ball_bearing = ball_bearing
		self.distance = distance

	def update(self, blade_side, distance):

		self.blade_side = blade_side
		self.distance = distance
