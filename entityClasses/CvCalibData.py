import Shapes




""" For P02 """
X_SMALL = 370
Y_SMALL = 156
X_LARGE = 350
Y_LARGE = 162
Y_MAX_SMALL = 200
Y_MIN_SMALL = 130
X_MAX_SMALL = 420
X_MIN_SMALL = 300
Y_MAX_LARGE = 200
Y_MIN_LARGE = 130
X_MAX_LARGE = 420
X_MIN_LARGE = 300
MIN_RAD_SMALL = 50
MAX_RAD_SMALL = 70 
MIN_RAD_LARGE = 70
MAX_RAD_LARGE = 80
RAD_LARGE = 69
RAD_SMALL = 54
CIRC_PARAM_LARGE = 1
CIRC_PARAM_SMALL = 4


""" Per blade side and bb size per stage (16 in total) """
class Calibrations(object):

	def __init__(self):



                """ ***************************** P02 Blisk Configurations ***************************** """
		""" CvCalibData(radius, radius_max, radius_min, x_init, y_init, y_max, y_min, x_max, x_min) """
		""" Set the shape locations for the calibration (x_offset,y_offset,x_width,y_width,angle) """
		
		""" Large BB size for P02 concave fillet """
		self.calib_P02_0_0_0 = CvCalibData(RAD_LARGE, MAX_RAD_LARGE, MIN_RAD_LARGE, 
			X_LARGE, Y_LARGE, Y_MAX_LARGE, Y_MIN_LARGE, Y_MAX_LARGE, Y_MIN_LARGE, CIRC_PARAM_LARGE)
		self.calib_P02_0_0_0.setShapes(1, 50,20,50,100,0)
		self.calib_P02_0_0_0.setShapes(2,38,-95,80,35,45)
		self.calib_P02_0_0_0.setShapes(3,-125,-60,90,70,-45)

		""" Large BB size for P02 convex fillet """
		self.calib_P02_0_1_0 = CvCalibData(RAD_LARGE, MAX_RAD_LARGE, MIN_RAD_LARGE, 
			X_LARGE, Y_LARGE, Y_MAX_LARGE, Y_MIN_LARGE, Y_MAX_LARGE, Y_MIN_LARGE, CIRC_PARAM_LARGE)
		self.calib_P02_0_1_0.setShapes(1, 60,20,70,100,20)
		self.calib_P02_0_1_0.setShapes(2,0,0,100,50,0)
		self.calib_P02_0_1_0.setShapes(3,-130,-40,70,100,0)

		""" Small BB size for P02 concave fillet """
		self.calib_P02_0_0_1 = CvCalibData(RAD_SMALL, MAX_RAD_SMALL, MIN_RAD_SMALL, 
			X_SMALL, Y_SMALL, Y_MAX_SMALL, Y_MIN_SMALL, Y_MAX_SMALL, Y_MIN_SMALL, CIRC_PARAM_SMALL)
		self.calib_P02_0_0_1.setShapes(1, 60,-70,70,70,20)
		self.calib_P02_0_0_1.setShapes(2,-50,-120,100,50,40)
		self.calib_P02_0_0_1.setShapes(3,-130,-40,70,70,45)

		""" Small BB size for P02 convex fillet """
		self.calib_P02_0_1_1 = CvCalibData(RAD_SMALL, MAX_RAD_SMALL, MIN_RAD_SMALL, 
			X_SMALL, Y_SMALL, Y_MAX_SMALL, Y_MIN_SMALL, Y_MAX_SMALL, Y_MIN_SMALL, CIRC_PARAM_SMALL)
		self.calib_P02_0_1_1.setShapes(1, 60,-70,70,70,20)
		self.calib_P02_0_1_1.setShapes(2,-50,-120,100,50,40)
		self.calib_P02_0_1_1.setShapes(3,-130,-40,70,70,45)



                """ ***************************** P01 Blisk Configurations ***************************** """
                """ CvCalibData(radius, radius_max, radius_min, x_init, y_init, y_max, y_min, x_max, x_min) """
		""" Set the shape locations for the calibration (x_offset,y_offset,x_width,y_width,angle) """
		
                """ Large BB size for P01 concave fillet """
		self.calib_P01_0_0_0 = CvCalibData(RAD_LARGE, MAX_RAD_LARGE, MIN_RAD_LARGE, 
			X_LARGE, Y_LARGE, Y_MAX_LARGE, Y_MIN_LARGE, Y_MAX_LARGE, Y_MIN_LARGE, CIRC_PARAM_LARGE)
		self.calib_P01_0_0_0.setShapes(1, 50,20,50,100,0)
		self.calib_P01_0_0_0.setShapes(2,38,-95,80,35,45)
		self.calib_P01_0_0_0.setShapes(3,-125,-60,90,70,-45)

		""" Large BB size for P01 convex fillet """
		self.calib_P01_0_1_0 = CvCalibData(RAD_LARGE, MAX_RAD_LARGE, MIN_RAD_LARGE, 
			X_LARGE, Y_LARGE, Y_MAX_LARGE, Y_MIN_LARGE, Y_MAX_LARGE, Y_MIN_LARGE, CIRC_PARAM_LARGE)
		self.calib_P01_0_1_0.setShapes(1, 60,20,70,100,20)
		self.calib_P01_0_1_0.setShapes(2,0,0,100,50,0)
		self.calib_P01_0_1_0.setShapes(3,-130,-40,70,100,0)
                
                """ Small BB size for P01 concave fillet """
		self.calib_P01_0_0_1 = CvCalibData(RAD_SMALL, MAX_RAD_SMALL, MIN_RAD_SMALL, 
			X_SMALL, Y_SMALL, Y_MAX_SMALL, Y_MIN_SMALL, Y_MAX_SMALL, Y_MIN_SMALL, CIRC_PARAM_SMALL)
		self.calib_P01_0_0_1.setShapes(1, 60,-70,70,70,20)
		self.calib_P01_0_0_1.setShapes(2,-50,-120,100,50,40)
		self.calib_P01_0_0_1.setShapes(3,-130,-40,70,70,45)

		""" Small BB size for P01 convex fillet """
		self.calib_P01_0_1_1 = CvCalibData(RAD_SMALL, MAX_RAD_SMALL, MIN_RAD_SMALL, 
			X_SMALL, Y_SMALL, Y_MAX_SMALL, Y_MIN_SMALL, Y_MAX_SMALL, Y_MIN_SMALL, CIRC_PARAM_SMALL)
		self.calib_P01_0_1_1.setShapes(1, 60,-70,70,70,20)
		self.calib_P01_0_1_1.setShapes(2,-50,-120,100,50,40)
		self.calib_P01_0_1_1.setShapes(3,-130,-40,70,70,45)



		""" ***************************** G02 Blisk Stage 0 Configurations ***************************** """
                """ CvCalibData(radius, radius_max, radius_min, x_init, y_init, y_max, y_min, x_max, x_min) """
		""" Set the shape locations for the calibration (x_offset,y_offset,x_width,y_width,angle) """
                
                """ Large BB size for G02 Stage 0 concave fillet """
		self.calib_G02_0_0_0 = CvCalibData(RAD_LARGE, MAX_RAD_LARGE, MIN_RAD_LARGE, 
			X_LARGE, Y_LARGE, Y_MAX_LARGE, Y_MIN_LARGE, Y_MAX_LARGE, Y_MIN_LARGE, CIRC_PARAM_LARGE)
		self.calib_G02_0_0_0.setShapes(1, 50,20,50,100,0)
		self.calib_G02_0_0_0.setShapes(2,38,-95,80,35,45)
		self.calib_G02_0_0_0.setShapes(3,-125,-60,90,70,-45)

		""" Large BB size for G02 Stage 0 convex fillet """
		self.calib_G02_0_1_0 = CvCalibData(RAD_LARGE, MAX_RAD_LARGE, MIN_RAD_LARGE, 
			X_LARGE, Y_LARGE, Y_MAX_LARGE, Y_MIN_LARGE, Y_MAX_LARGE, Y_MIN_LARGE, CIRC_PARAM_LARGE)
		self.calib_G02_0_1_0.setShapes(1, 60,20,70,100,20)
		self.calib_G02_0_1_0.setShapes(2,0,0,100,50,0)
		self.calib_G02_0_1_0.setShapes(3,-130,-40,70,100,0)

		""" Small BB size for G02 Stage 0 concave fillet """
		self.calib_G02_0_0_1 = CvCalibData(RAD_SMALL, MAX_RAD_SMALL, MIN_RAD_SMALL, 
			X_SMALL, Y_SMALL, Y_MAX_SMALL, Y_MIN_SMALL, Y_MAX_SMALL, Y_MIN_SMALL, CIRC_PARAM_SMALL)
		self.calib_G02_0_0_1.setShapes(1, 60,-70,70,70,20)
		self.calib_G02_0_0_1.setShapes(2,-50,-120,100,50,40)
		self.calib_G02_0_0_1.setShapes(3,-130,-40,70,70,45)

		""" Small BB size for G02 Stage 0 convex fillet """
		self.calib_G02_0_1_1 = CvCalibData(RAD_SMALL, MAX_RAD_SMALL, MIN_RAD_SMALL, 
			X_SMALL, Y_SMALL, Y_MAX_SMALL, Y_MIN_SMALL, Y_MAX_SMALL, Y_MIN_SMALL, CIRC_PARAM_SMALL)
		self.calib_G02_0_1_1.setShapes(1, 60,-70,70,70,20)
		self.calib_G02_0_1_1.setShapes(2,-50,-120,100,50,40)
		self.calib_G02_0_1_1.setShapes(3,-130,-40,70,70,45)




		""" ***************************** G02 Blisk Stage 1 Configurations ***************************** """
                """ CvCalibData(radius, radius_max, radius_min, x_init, y_init, y_max, y_min, x_max, x_min) """
		""" Set the shape locations for the calibration (x_offset,y_offset,x_width,y_width,angle) """
                
                """ Large BB size for G02 Stage 1 concave fillet """
		self.calib_G02_1_0_0 = CvCalibData(RAD_LARGE, MAX_RAD_LARGE, MIN_RAD_LARGE, 
			X_LARGE, Y_LARGE, Y_MAX_LARGE, Y_MIN_LARGE, Y_MAX_LARGE, Y_MIN_LARGE, CIRC_PARAM_LARGE)
		self.calib_G02_1_0_0.setShapes(1, 50,20,50,100,0)
		self.calib_G02_1_0_0.setShapes(2,38,-95,80,35,45)
		self.calib_G02_1_0_0.setShapes(3,-125,-60,90,70,-45)

		""" Large BB size for G02 Stage 1 convex fillet """
		self.calib_G02_1_1_0 = CvCalibData(RAD_LARGE, MAX_RAD_LARGE, MIN_RAD_LARGE, 
			X_LARGE, Y_LARGE, Y_MAX_LARGE, Y_MIN_LARGE, Y_MAX_LARGE, Y_MIN_LARGE, CIRC_PARAM_LARGE)
		self.calib_G02_1_1_0.setShapes(1, 60,20,70,100,20)
		self.calib_G02_1_1_0.setShapes(2,0,0,100,50,0)
		self.calib_G02_1_1_0.setShapes(3,-130,-40,70,100,0)

		""" Small BB size for G02 Stage 1 concave fillet """
		self.calib_G02_1_0_1 = CvCalibData(RAD_SMALL, MAX_RAD_SMALL, MIN_RAD_SMALL, 
			X_SMALL, Y_SMALL, Y_MAX_SMALL, Y_MIN_SMALL, Y_MAX_SMALL, Y_MIN_SMALL, CIRC_PARAM_SMALL)
		self.calib_G02_1_0_1.setShapes(1, 60,-70,70,70,20)
		self.calib_G02_1_0_1.setShapes(2,-50,-120,100,50,40)
		self.calib_G02_1_0_1.setShapes(3,-130,-40,70,70,45)

		""" Small BB size for G02 Stage 1 convex fillet """
		self.calib_G02_1_1_1 = CvCalibData(RAD_SMALL, MAX_RAD_SMALL, MIN_RAD_SMALL, 
			X_SMALL, Y_SMALL, Y_MAX_SMALL, Y_MIN_SMALL, Y_MAX_SMALL, Y_MIN_SMALL, CIRC_PARAM_SMALL)
		self.calib_G02_1_1_1.setShapes(1, 60,-70,70,70,20)
		self.calib_G02_1_1_1.setShapes(2,-50,-120,100,50,40)
		self.calib_G02_1_1_1.setShapes(3,-130,-40,70,70,45)
































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

		""" Shape width and heights """
		self.shape1_width = 0
		self.shape1_height = 0
		self.shape2_width = 0
		self.shape2_height = 0
		self.shape3_width = 0
		self.shape3_height = 0

		""" Shape x and y coordinates """
		self.shape1_x = 0
		self.shape1_y = 0
		self.shape2_x = 0
		self.shape2_y = 0
		self.shape3_x = 0
		self.shape3_y = 0

		""" Shape angles """
		self.shape1_angle = 0
		self.shape2_angle = 0
		self.shape3_angle = 0

		""" Make the Boxes to search for light in """
		self.shap1 = None
		self.shape2 = None
		self.shape3 = None

	def setShapes(self,shapeNum,x_offset,y_offset,x_width,y_width, angle):

		if shapeNum == 1:
			self.shape1_x = x_offset
			self.shape1_y = y_offset
			self.shape1_width = x_width
			self.shape1_height = y_width
			self.shape1_angle = angle
			self.shape1 = Shapes.AngledBox(self.x_init + self.shape1_x, self.y_init + self.shape1_y, self.shape1_width, self.shape1_height, angle)
		elif shapeNum == 2:
			self.shape2_x = x_offset
			self.shape2_y = y_offset
			self.shape2_width = x_width
			self.shape2_height = y_width
			self.shape2_angle = angle
			self.shape2 = Shapes.AngledBox(self.x_init + self.shape2_x, self.y_init + self.shape2_y, self.shape2_width, self.shape2_height, angle)
		elif shapeNum == 3:
			self.shape3_x = x_offset
			self.shape3_y = y_offset
			self.shape3_width = x_width
			self.shape3_height = y_width
			self.shape3_angle = angle
			self.shape3 = Shapes.AngledBox(self.x_init + self.shape3_x, self.y_init + self.shape3_y, self.shape3_width, self.shape3_height, angle)
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
