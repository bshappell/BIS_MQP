# ImageProcessor Class
import cv2
import numpy as np
import InspectionResults
import sys
import time

DEBUG = 1 # Toggle to get debug features
RASP_PI = 1 # Indicates whether 
CAMERA = 1 # Indicates whether to run the code with the camera

HUE_LOW = 26
HUE_HIGH = 71
SATURATION_LOW = 105
SATURATION_HIGH = 255
VALUE_LOW = 100 #116
VALUE_HIGH = 255

class ImageProcessor(object):

	def __init__(self):


		if RASP_PI:
			self.capture = cv2.VideoCapture(0)
		else:
			self.capture = cv2.VideoCapture(1)
		self.frame = None

		""" Inspection Results Class """
		self.results = InspectionResults.InspectionResults()

		""" Define the range of green to mask """
		self.lower_green = np.array([HUE_LOW,SATURATION_LOW,VALUE_LOW])
		self.upper_green = np.array([HUE_HIGH,SATURATION_HIGH,VALUE_HIGH])

		""" The Different Boxes to search for light in """
		self.box1 = Box(80,80,100,100)
		self.box2 = Box(50,270,100,100)
		self.box3 = Box(250,320,100,100)

		""" Array of Test Images """
		frame1 = cv2.imread('..\\better_pics\\Up2Covered.jpg',-1)
		frame2 = cv2.imread('..\\better_pics\\Up2Uncovered.jpg',-1)
		frame3 = cv2.imread('..\\better_pics\\Down1Covered.jpg',-1)
		frame4 = cv2.imread('..\\better_pics\\Down1Uncovered.jpg',-1)
		frame5 = cv2.imread('..\\better_pics\\Down2Covered.jpg',-1)
		frame6 = cv2.imread('..\\better_pics\\Down2Uncovered.jpg',-1)
		frame7 = cv2.imread('..\\better_pics\\Up1Uncovered.jpg',-1)
		frame8 = cv2.imread('..\\better_pics\\Up1Covered.jpg',-1)
		self.frames = [frame1,frame2,frame3,frame4,frame5,frame6,frame7,frame8]

	""" Find the Ball Bearing and locate the centroid """
	def findBB(self, image):

		img = cv2.imread(image,0)
		img = cv2.medianBlur(img,5)
		cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

		circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT,1,20,
		                            param1=50,param2=45,minRadius=80,maxRadius=0)

		circles = np.uint16(np.around(circles))
		for i in circles[0,:]:
		    # draw the outer circle
		    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
		    # draw the center of the circle
		    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

		cv2.imshow('detected circles',cimg)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	""" Find the Ball Bearing and locate the centroid """
	def findBBCamera(self):

		ret, self.frame = self.capture.read()

		""" Convert BGR to HSV """
		cimg = cv2.cvtColor(self.frame, cv2.COLOR_GRAY2BGR)

		#ret, pic = self.capture.read()
		#img = cv2.imread(pic,0)
		#img = cv2.medianBlur(pic,5)
		#cimg = cv2.cvtColor(pic, cv2.COLOR_GRAY2BGR)

		circles = cv2.HoughCircles(self.frame, cv2.cv.CV_HOUGH_GRADIENT,1,20, param1=50,param2=45,minRadius=80,maxRadius=0)

		circles = np.uint16(np.around(circles))
		for i in circles[0,:]:
		    # draw the outer circle
		    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
		    # draw the center of the circle
		    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

		cv2.imshow('detected circles',cimg)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		

	""" Inspect the test array of images """
	def inspectArray(self):

		for frame in self.frames:
			self.inspectImage(True,frame)

		if DEBUG:
			while(True):
				cnt = 0
				for frame in self.frames:
					cv2.imshow('Inspected Image ' + str(cnt),frame)
					cnt += 1
				key = cv2.waitKey(1) & 0xFF
				if key == ord('q'):
					break
		
		""" Close all windows currently open """
		self.shutdown()

	def inspect(self, isSmallBB, callFunction, bliskNum, stageNum):

                start_time = time.time()
                pic_count = 0

		while(callFunction(bliskNum, stageNum)):

			self.inspectImageFromCamera(True)
			cv2.imshow('Inspected Camera Image ',self.frame)

			key = cv2.waitKey(1) & 0xFF

			pic_count += 1

                end_time =(time.time())
                self.my_print("end_time: ")
                self.my_print(end_time)
		self.my_print("start_time: ")
		self.my_print(start_time)
		self.my_print("elapsed time: ")
		self.my_print(end_time - start_time)
		self.my_print("pic_count: ")
		self.my_print(pic_count)
		self.my_print("fps: ")
		self.my_print(pic_count/(end_time - start_time))
		



	""" Inspect Camera image """
	def inspectCameraImage(self):

		while(True):

			self.inspectImageFromCamera(True)
			#self.findBBCamera()
			"""cv2.imshow('Inspected Camera Image ',self.frame)

			key = cv2.waitKey(1) & 0xFF
			if key == ord('q'):
				break"""
		
		""" Close all windows currently open """
		self.shutdown()


	""" Inspect the current image to see if it passes """
	def inspectImage(self, isSmallBB, frame): #, currStage, sizeBB):

		imagePasses = False
		frame_init = frame.copy()

		""" Convert BGR to HSV """
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		""" Threshold the HSV image to get only green colors """
		mask = cv2.inRange(hsv, self.lower_green, self.upper_green)

		""" Bitwise-AND mask and original image """
		res = cv2.bitwise_and(frame,frame, mask= mask)

		""" Find the Contours in the Mask """
		(cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

		""" Initialize the counts of contours in each section to zero """
		quad1_cnt = 0
		quad2_cnt = 0
		quad3_cnt = 0
		 
		""" Iterate over each of the contours """
		for c in cnts:

			""" compute the center of the contour """
			M = cv2.moments(c)
			area = M["m00"]
			if M["m00"] == 0:
				area = 0.000001
			cX = int(M["m10"] / area)
			cY = int(M["m01"] / area)

			if DEBUG:
				""" draw the contour and center of the shape on the image """
				cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
				cv2.circle(frame, (cX, cY), 7, (0, 0, 0), -1)

				""" Draw the Boxes around each of the areas """
				self.box1.draw(frame)
				self.box2.draw(frame)
				self.box3.draw(frame)

			""" Determine the number of centroids in each quadrant """
			if self.box1.inBox(cX,cY):
				quad1_cnt += 1
			elif self.box2.inBox(cX,cY):
				quad2_cnt += 1
			elif self.box3.inBox(cX,cY):
				quad3_cnt += 1

		""" Determine if the ball bearing case sizes pass """
		imagePasses = self.checkImage(isSmallBB,quad1_cnt,quad2_cnt,quad3_cnt)

		""" Indicate Whether the image passes or fails """
		cv2.putText(frame, "Inspection Passes: " + str(imagePasses), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.upper_green, 2)

		return imagePasses

	""" Determine if the centroid count in each quadrant passes """
	def checkImage(self,isSmallBB,quad1_cnt,quad2_cnt,quad3_cnt):

		if isSmallBB:
			return self.checkSmallBB(quad1_cnt,quad2_cnt,quad3_cnt)
		else:
			return self.checkLargeBB(quad1_cnt,quad2_cnt,quad3_cnt)

	""" Check to see if the image passes with the large BB size """
	def checkLargeBB(self,quad1_cnt,quad2_cnt,quad3_cnt):

		if ((quad1_cnt>0) and (quad3_cnt>0)):
			return True
		return False

	""" Check to see if the image passes with the Small BB size """
	def checkSmallBB(self,quad1_cnt,quad2_cnt,quad3_cnt):	

		if ((quad1_cnt>0) and (quad2_cnt>0) and (quad3_cnt>0)):
			return True
		return False	


	""" When everything done, release the capture """
	def shutdown(self):
		if CAMERA:
			self.capture.release()
		cv2.destroyAllWindows()
		if CAMERA:
			self.capture.release()


	""" Inspect the current image to see if it passes """
	def inspectImageFromCamera(self, isSmallBB): #, currStage, sizeBB):

		imagePasses = False
		#frame_init = frame.copy()
		ret, self.frame = self.capture.read()

		""" Convert BGR to HSV """
		hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

		""" Threshold the HSV image to get only green colors """
		mask = cv2.inRange(hsv, self.lower_green, self.upper_green)

		""" Bitwise-AND mask and original image """
		res = cv2.bitwise_and(self.frame,self.frame, mask= mask)

		""" Find the Contours in the Mask """
		if RASP_PI:
			(_, cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		else:
			(cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

		""" Initialize the counts of contours in each section to zero """
		quad1_cnt = 0
		quad2_cnt = 0
		quad3_cnt = 0
		 
		""" Iterate over each of the contours """
		for c in cnts:

			""" compute the center of the contour """
			M = cv2.moments(c)
			area = M["m00"]
			if M["m00"] == 0:
				area = 0.000001
			cX = int(M["m10"] / area)
			cY = int(M["m01"] / area)

			if DEBUG:
				""" draw the contour and center of the shape on the image """
				cv2.drawContours(self.frame, [c], -1, (0, 255, 0), 2)
				cv2.circle(self.frame, (cX, cY), 7, (0, 0, 0), -1)

				""" Draw the Boxes around each of the areas """
				self.box1.draw(self.frame)
				self.box2.draw(self.frame)
				self.box3.draw(self.frame)

			""" Determine the number of centroids in each quadrant """
			if self.box1.inBox(cX,cY):
				quad1_cnt += 1
			elif self.box2.inBox(cX,cY):
				quad2_cnt += 1
			elif self.box3.inBox(cX,cY):
				quad3_cnt += 1

		""" Determine if the ball bearing case sizes pass """
		imagePasses = self.checkImage(isSmallBB,quad1_cnt,quad2_cnt,quad3_cnt)

		""" Indicate Whether the image passes or fails """
		cv2.putText(self.frame, "Inspection Passes: " + str(imagePasses), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.upper_green, 2)

		return imagePasses

	def test(self):

                cap = self.capture

                while(cap.isOpened()):
                        ret, frame = cap.read()

                        cv2.imshow('frame', frame)
                        key = cv2.waitKey(1) & 0xFF
			if key == ord('q'):
				break

		cap.release()
		cv2.destroyAllWindows()

	""" Function to handle system prints """
	def my_print(self, text):
	    sys.stdout.write(str(text))
	    sys.stdout.flush()


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
				return 1

		""" Otherwise return False """
		return 0

	""" Draw the Box from the Points on the given image """
	def draw(self, frame):

		cv2.line(frame, self.p00(), self.p01(), self.color)
		cv2.line(frame, self.p00(), self.p10(), self.color)
		cv2.line(frame, self.p11(), self.p01(), self.color)
		cv2.line(frame, self.p11(), self.p10(), self.color)


""" Used for testing purposes """
if __name__ == "__main__":

	ip = ImageProcessor()
	#ip.test()
	ip.inspectCameraImage()
	#ip.inspectArray()
        #ip.findBBCamera()

	"""ip.findBB('..\\better_pics\\Up2Covered.jpg')
	ip.findBB('..\\better_pics\\Up2Uncovered.jpg')
	ip.findBB('..\\better_pics\\Up1Uncovered.jpg')
	ip.findBB('..\\better_pics\\Up1Covered.jpg')"""

	"""results = InspectionResults.InspectionResults()
	results.openNewFile("22")
	results.addResult(1,2,3,4,'yo')
	results.closeFile()"""














		
