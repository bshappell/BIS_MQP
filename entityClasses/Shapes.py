



""" Box Object to Store 4 points, draw the box and determine if points are within the box """
class Box(object):

	def __init__(self, x_pos, y_pos, x_width, y_width, filled):

		""" Store the parameter values """
		self.xPos = x_pos
		self.yPos = y_pos
		self.xWidth = x_width
		self.yWidth = y_width
		self.filled = filled

		if(self.filled):
			""" Color to draw the box lines """
			self.color = (255,255,255)
		else:
			self.color = (0, 0, 255)

	""" Return the Upper Left Hand Point on the Box """
	def p00(self):
		return (self.xPos,self.yPos)

	""" Return the Lower Left Hand Point on the Box """
	def p01(self):
		return (self.xPos,self.yPos + self.yWidth)

	""" Return the Upper Right Hand Point on the Box """
	def p10(self):
		return (self.xPos + self.xWidth, self.yPos)

	""" Return the Lower Right Hand Point on the Box """
	def p11(self):
		return (self.xPos + self.xWidth, self.yPos + self.yWidth)

	""" Returns a Boolean Indicating whether the given x,y coordinates are within the box """
	def inBox(self, x_pos, y_pos):

		""" Check that the x and y values are in the correct range """
		if((x_pos >= self.xPos) and (x_pos <= (self.xPos + self.xWidth))):
			if((y_pos >= self.yPos) and (y_pos <= (self.yPos + self.yWidth))):
				return 1

		""" Otherwise return False """
		return 0

	""" Draw the Box from the Points on the given image """
	def draw(self, frame):

		cv2.line(frame, self.p00(), self.p01(), self.color)
		cv2.line(frame, self.p00(), self.p10(), self.color)
		cv2.line(frame, self.p11(), self.p01(), self.color)
		cv2.line(frame, self.p11(), self.p10(), self.color)
		