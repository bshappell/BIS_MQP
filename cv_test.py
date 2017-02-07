
import numpy as np
import cv2


def simpleImage():

	# Load an color image 0 = grayscale, 1 = colored, -1 = unchanged
	img = cv2.imread('cuteCat.jpg',0)

	# display an image (img) in the window named 'Cat Pic'
	cv2.imshow('Cat Pic',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


def catPic():

	img = cv2.imread('cuteCat.jpg',0)
	cv2.imshow('Grey Cat',img)
	k = cv2.waitKey(0) & 0xFF
	if k == 27:         # wait for ESC key to exit
	    cv2.destroyAllWindows()
	elif k == ord('s'): # wait for 's' key to save and exit
	    cv2.imwrite('greyCat.png',img)
	    cv2.destroyAllWindows()

def camTest():

	cap = cv2.VideoCapture(1)

	while(True):
	    # Capture frame-by-frame
	    ret, frame = cap.read()

	    # Our operations on the frame come here
	    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	    # Display the resulting frame
	    cv2.imshow('frame',gray)
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

def captureImage():

	cap = cv2.VideoCapture(1)
	imageCount = 0 # used to increment picture counts 

	while(True):
	    # Capture frame-by-frame
	    ret, frame = cap.read()

	    # Our operations on the frame come here
	    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	    # Display the resulting frame
	    cv2.imshow('frame',frame)
	    key = cv2.waitKey(1) & 0xFF
	    if key == ord('q'):
	        break
	    # Save the Image if we receive an s key press
	    elif key == ord('s'):
	    	imageCount += 1 # increment the image count variable
	    	cv2.imwrite('capture' + str(imageCount) + '.png',frame)

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()
	cap.release()


def detectSWs():

	frame = cv2.imread('better_pics\\Up2Covered.jpg',-1)
	frame_init = frame.copy()

	# Convert BGR to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# define range of blue color in HSV
	lower_green = np.array([26,105,116])
	upper_green = np.array([71,255,255])

	# Threshold the HSV image to get only blue colors
	mask = cv2.inRange(hsv, lower_green, upper_green)

	# Bitwise-AND mask and original image
	res = cv2.bitwise_and(frame,frame, mask= mask)

	# find the contours in the mask
	(cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	print "I found %d green shapes" % (len(cnts))
	 
	# loop over the contours
	for c in cnts:

		# compute the center of the contour
		M = cv2.moments(c)
		if M["m00"] == 0:
			print "Zero denominator found for contour " + str(c)
			area = 0.000001
			print str(M["m10"])
			print str(M["m01"])
			#cX = 0
			#cY = 0
		else:
			#cX = int(M["m10"] / M["m00"])
			#cY = int(M["m01"] / M["m00"])
			area = M["m00"]

		cX = int(M["m10"] / area)
		cY = int(M["m01"] / area)

		print "Contour Area: " + str(area)
		print "Contour cx: " + str(cX) + " cy: " + str(cY)
	 
		# draw the contour and center of the shape on the image
		cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
		cv2.circle(frame, (cX, cY), 7, (0, 0, 0), -1)
		cv2.putText(frame, "center", (cX - 20, cY - 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

	while(True):
		cv2.imshow('Outlined Shapes',frame)
		cv2.imshow('Result',res)
		cv2.imshow('Shape Mask',mask)
		cv2.imshow('Initial Frame',frame_init)
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			break
	
	# Close all windows currently open
	cv2.destroyAllWindows()	



HUE_LOW = 26
HUE_HIGH = 71
SATURATION_LOW = 105
SATURATION_HIGH = 255
VALUE_LOW = 116
VALUE_HIGH = 255

SHOW_IMAGE = 1 # Toggle to either display the images or not

def inspectImage():


	frame = cv2.imread('better_pics\\Up2Covered.jpg',-1)
	frame_init = frame.copy()

	""" Convert BGR to HSV """
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	""" Define the range of green to mask """
	lower_green = np.array([HUE_LOW,SATURATION_LOW,VALUE_LOW])
	upper_green = np.array([HUE_HIGH,SATURATION_HIGH,VALUE_HIGH])

	""" Threshold the HSV image to get only green colors """
	mask = cv2.inRange(hsv, lower_green, upper_green)

	""" Bitwise-AND mask and original image """
	res = cv2.bitwise_and(frame,frame, mask= mask)

	""" Find the Contours in the Mask """
	(cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	num_shapes = len(cnts)
	print "I found %d green shapes" % (num_shapes)
	 
	""" Iterate over each of the contours """
	for c in cnts:

		# compute the center of the contour
		M = cv2.moments(c)
		if M["m00"] == 0:
			print "Zero denominator found for contour " + str(c)
			area = 0.000001
			print str(M["m10"])
			print str(M["m01"])
			#cX = 0
			#cY = 0
		else:
			#cX = int(M["m10"] / M["m00"])
			#cY = int(M["m01"] / M["m00"])
			area = M["m00"]

		cX = int(M["m10"] / area)
		cY = int(M["m01"] / area)

		print "Contour Area: " + str(area)
		print "Contour cx: " + str(cX) + " cy: " + str(cY)
	 
		# draw the contour and center of the shape on the image
		cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
		cv2.circle(frame, (cX, cY), 7, (0, 0, 0), -1)

		box1 = Box(80,80,100,100)
		box1.draw(frame)

		box2 = Box(50,270,100,100)
		box2.draw(frame)

		box3 = Box(250,320,100,100)
		box3.draw(frame)

		cv2.putText(frame, "center", (cX - 20, cY - 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

	while(True):
		cv2.imshow('Outlined Shapes',frame)
		cv2.imshow('Result',res)
		cv2.imshow('Shape Mask',mask)
		cv2.imshow('Initial Frame',frame_init)
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			break
	
	""" Close all windows currently open """
	cv2.destroyAllWindows()	


""" Box Object to Store 4 points, draw the box and determine if points are within the box """
class Box(object):

	def __init__(self, x_pos, y_pos, x_width, y_width):

		""" Store the parameter values """
		self.xPos = x_pos
		self.yPos = y_pos
		self.xWidth = x_width
		self.yWidth = y_width

		""" Color to draw the box lines """
		self.color = (255,255,255)

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
				return True

		""" Otherwise return False """
		return False

	""" Draw the Box from the Points on the given image """
	def draw(self, frame):

		cv2.line(frame, self.p00(), self.p01(), self.color)
		cv2.line(frame, self.p00(), self.p10(), self.color)
		cv2.line(frame, self.p11(), self.p01(), self.color)
		cv2.line(frame, self.p11(), self.p10(), self.color)



if __name__=="__main__":

	inspectImage()
