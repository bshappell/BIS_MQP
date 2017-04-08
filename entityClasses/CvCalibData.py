import Shapes

""" Per blade side and bb size per stage (16 in total) """
class CvCalibData(object):

	def __init__(self, radius, radius_max, radius_min, x_init, y_init, y_max, y_min, x_max, x_min, circles_param):

		""" Ball gauge radius dimensions """
		self.radius = radius
		self.radius_max = radius_max
		self.radius_min = radius_min

		""" Ball Gauge location in the image """
		self.x_init = x_init
		self.y_init = y_init
		self.bb_x = x_init
		self.bb_y = y_init
		self.y_max = y_max
		self.y_min = y_min
		self.x_max = x_max
		self.x_min = x_min
		self.circles_param = circles_param

		""" Shape positions """
		self.shape1_width = 70
		self.shape1_height = 70
		self.shape2_width = 100
		self.shape2_height = 50
		self.shape3_width = 70
		self.shape3_height = 70

		self.shape1_x = -30
		self.shape1_y = -70
		self.shape2_x = -120
		self.shape2_y = -100
		self.shape3_x = -180
		self.shape3_y = 20

		""" Make the Boxes to search for light in """
		self.shape1 = Shapes.Box(x_init + self.shape1_x, y_init + self.shape1_y, self.shape1_width, self.shape1_height, True)
		self.shape2 = Shapes.Box(x_init + self.shape2_x, y_init + self.shape2_y, self.shape2_width, self.shape2_height, True)
		self.shape3 = Shapes.Box(x_init + self.shape3_x, y_init + self.shape3_y, self.shape3_width, self.shape3_height, True)

	def setShapes(self,shapeNum,x_offset,y_offset,x_width,y_width):

		if shapeNum == 1:
			self.shape1_x = x_offset
			self.shape1_y = y_offset
			self.shape1_width = x_width
			self.shape1_height = y_width
		elif shapeNum == 2:
			self.shape2_x = x_offset
			self.shape2_y = y_offset
			self.shape2_width = x_width
			self.shape2_height = y_width
		elif shapeNum == 3:
			self.shape3_x = x_offset
			self.shape3_y = y_offset
			self.shape3_width = x_width
			self.shape3_height = y_width
		else:
			print "ERROR INCORRECT SHAPE NUMBER RECEIVED IN SET SHAPES"

	def update(self, radius, radius_max, radius_min, x_init, y_init, y_max, y_min, x_max, x_min, circles_param):

		""" Ball gauge radius dimensions """
		self.radius = radius
		self.radius_max = radius_max
		self.radius_min = radius_min

		""" Ball Gauge location in the image """
		self.x_init = x_init
		self.y_init = y_init
		self.y_max = y_max
		self.y_min = y_min
		self.x_max = x_max
		self.x_min = x_min
		self.circles_param = circles_param

	def checkCircle(self, x, y, r):

		if(r>self.radius_min) and (r<self.radius_max) and (y<self.y_max) and (y>self.y_min) and (x<self.x_max) and (x>self.x_min):
			return True
		return False

	""" Update the shape locations based on the ball bearing location """
	def updateShapeLocations(self, x, y):

		self.bb_x = x 
		self.bb_y = y
		self.shape1.update(self.bb_x + self.shape1_x, self.bb_y + self.shape1_y, self.shape1_width, self.shape1_height)
		self.shape2.update(self.bb_x + self.shape2_x, self.bb_y + self.shape2_y, self.shape2_width, self.shape2_height)
		self.shape3.update(self.bb_x + self.shape3_x, self.bb_y + self.shape3_y, self.shape3_width, self.shape3_height)


	""" Returns whether a point is within the defined shape """
	def inShape(self, shapeNum, x, y):

		if shapeNum == 1:
			return self.shape1.inBox(x,y)
		elif shapeNum == 2:
			return self.shape2.inBox(x,y)
		elif shapeNum == 3:
			return self.shape3.inBox(x,y)
		else:
			print "ERROR INCORRECT SHAPE NUMBER RECEIVED"

	def drawShapes(self, frame):

		self.shape1.draw(frame)
		self.shape2.draw(frame)
		self.shape3.draw(frame)
