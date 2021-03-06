# ImageProcessor Class
import cv2
import numpy as np
import InspectionResults
import InspectionPosition
import sys
import time
import CvCalibData
import math

DEBUG = 1 # Toggle to get debug features
RASP_PI = 1 # Indicates whether the code is running on the Raspberry Pi or not
CAMERA = 1 # Indicates whether to run the code with the camera
VIDEO = 0 # Indicates if a video should be recorded
IMAGE_CAPTURE = 1

HUE_LOW = 30 #26
HUE_HIGH = 90
SATURATION_LOW = 150
SATURATION_HIGH = 255
VALUE_LOW = 180 #116
VALUE_HIGH = 255

WEIGHT = 7 


class ImageProcessor(object):

	def __init__(self):

		if RASP_PI:
			self.capture = cv2.VideoCapture(0)
		else:
			self.capture = cv2.VideoCapture(1)
		self.frame = None

		if IMAGE_CAPTURE:
			self.frame1 = None
			self.frame2 = None
			self.frame3 = None

		""" Inspection Results Class """
		self.results = InspectionResults.InspectionResults()

		""" Define the range of green to mask """
		self.lower_green = np.array([HUE_LOW,SATURATION_LOW,VALUE_LOW])
		self.upper_green = np.array([HUE_HIGH,SATURATION_HIGH,VALUE_HIGH])

		""" Calibrations stores each of the blisk configs """
                self.calibs = CvCalibData.Calibrations()

		""" Store the current calibration """
		self.current_calib = self.calibs.calib_P02_0_0_0
		self.ball_bearing_x = self.current_calib.x_init
		self.ball_bearing_y = self.current_calib.y_init

		
	""" Called before inspecting a new blisk """
	def newBlisk(self,bliskNum):

		if bliskNum == 0:
			bliskStr = "P01"
		elif bliskNum == 1:
			bliskStr = "P02"
		elif bliskNum == 2:
			bliskStr = "G02"

		""" Open new file for inspection results """
		self.results.openNewFile(bliskStr)

	""" Set the current calibration """
	def setCalibration(self, pos):

                """ The P02 blisk calibrations """
		if pos.blisk_number == 1 and pos.stage_number == 0 and pos.blade_side == 0 and pos.ball_bearing == 0:
			self.current_calib = self.calibs.calib_P02_0_0_0
		elif pos.blisk_number == 1 and pos.stage_number == 0 and pos.blade_side == 1 and pos.ball_bearing == 0:
			self.current_calib = self.calibs.calib_P02_0_1_0
		elif pos.blisk_number == 1 and pos.stage_number == 0 and pos.blade_side == 0 and pos.ball_bearing == 1:
			self.current_calib = self.calibs.calib_P02_0_0_1
		elif pos.blisk_number == 1 and pos.stage_number == 0 and pos.blade_side == 1 and pos.ball_bearing == 1:
			self.current_calib = self.calibs.calib_P02_0_1_1

                        """ The P01 blisk calibrations """
		elif pos.blisk_number == 0 and pos.stage_number == 0 and pos.blade_side == 0 and pos.ball_bearing == 0:
			self.current_calib = self.calibs.calib_P01_0_0_0
		elif pos.blisk_number == 0 and pos.stage_number == 0 and pos.blade_side == 1 and pos.ball_bearing == 0:
			self.current_calib = self.calibs.calib_P01_0_1_0
		elif pos.blisk_number == 0 and pos.stage_number == 0 and pos.blade_side == 0 and pos.ball_bearing == 1:
			self.current_calib = self.calibs.calib_P01_0_0_1
		elif pos.blisk_number == 0 and pos.stage_number == 0 and pos.blade_side == 1 and pos.ball_bearing == 1:
			self.current_calib = self.calibs.calib_P01_0_1_1

                        """ The G02 blisk stage 0 calibrations """
		elif pos.blisk_number == 2 and pos.stage_number == 0 and pos.blade_side == 0 and pos.ball_bearing == 0:
			self.current_calib = self.calibs.calib_G02_0_0_0
		elif pos.blisk_number == 2 and pos.stage_number == 0 and pos.blade_side == 1 and pos.ball_bearing == 0:
			self.current_calib = self.calibs.calib_G02_0_1_0
		elif pos.blisk_number == 2 and pos.stage_number == 0 and pos.blade_side == 0 and pos.ball_bearing == 1:
			self.current_calib = self.calibs.calib_G02_0_0_1
		elif pos.blisk_number == 2 and pos.stage_number == 0 and pos.blade_side == 1 and pos.ball_bearing == 1:
			self.current_calib = self.calibs.calib_G02_0_1_1

                        """ The G02 blisk stage 1 calibrations """
		elif pos.blisk_number == 2 and pos.stage_number == 1 and pos.blade_side == 0 and pos.ball_bearing == 0:
			self.current_calib = self.calibs.calib_G02_1_0_0
		elif pos.blisk_number == 2 and pos.stage_number == 1 and pos.blade_side == 1 and pos.ball_bearing == 0:
			self.current_calib = self.calibs.calib_G02_1_1_0
		elif pos.blisk_number == 2 and pos.stage_number == 1 and pos.blade_side == 0 and pos.ball_bearing == 1:
			self.current_calib = self.calibs.calib_G02_1_0_1
		elif pos.blisk_number == 2 and pos.stage_number == 1 and pos.blade_side == 1 and pos.ball_bearing == 1:
			self.current_calib = self.calibs.calib_G02_1_1_1

			
		else:
			print "ERROR IMAGE PROCESSOR CALIBRATION NOT FOUND"

	def inspect(self, callFunction, position):

		if VIDEO:
			video = cv2.VideoWriter('output.avi',-1, 7, (640,480))

		""" Set the correct calibration """
		self.setCalibration(position)

		""" Initialize the ball bearing position """
		self.ball_bearing_x = self.current_calib.x_init
		self.ball_bearing_y = self.current_calib.y_init

		image_count = 1
		pic_count = 0
		start_time = time.time()

		""" Inspection initially paused until start is received """
		if callFunction:
			pauseInspection = True
		else:
			pauseInspection = False
		stillInspecting = True
		inspectingUp = True
		while(stillInspecting):

			if callFunction:
				stillInspecting, message = callFunction(position)
				if message == "START_PATH_UP":
					inspectingUp = True
					pauseInspection = False
					self.my_print("START_PATH_UP RECEIVED\n")
				elif message == "START_PATH_DOWN":
					inspectingUp = False
					pauseInspection = False
					self.my_print("START_PATH_DOWN RECEIVED\n")
				elif message == "PAUSE_PATH":
					pauseInspection = True
					self.my_print("PAUSE_PATH RECEIVED\n")
				elif message:
					#position.update(distance)
					#self.setCalibration(position)
					self.my_print("POSITION RECEIVED: ")
					self.my_print(message)
					self.my_print("\n")

			""" Inspect the captured image """
			if(not pauseInspection):
				passValue = self.inspectImageFromCamera(position.ball_bearing, inspectingUp)
				cv2.imshow('Inspected Camera Image ', self.frame)

				if VIDEO:
					output = self.frame.copy()
					video.write(output)

				""" Save the inspection results to the file """
				if RASP_PI:
					self.results.addResult(position, passValue)

			pic_count += 1
			key = cv2.waitKey(1) & 0xFF
			if key == ord('q'):
                                if IMAGE_CAPTURE:
                                        break
			elif key == ord('s'):

				if IMAGE_CAPTURE:
					image_count += 1
					img = self.frame1
					cv2.imwrite("../pictures/Poster_1_" + str(image_count) +".png", img)
					img = self.frame2
					cv2.imwrite("../pictures/Poster_2_" + str(image_count) +".png", img)
					img = self.frame3
					cv2.imwrite("../pictures/Poster_3_" + str(image_count) +".png", img)

				else:
					image_count += 1
					img = self.frame
					cv2.imwrite("../pictures/Capture_" + str(image_count) +".png", img) 

		self.my_print("IMAGE PROCESSOR FPS: " + str(pic_count/(time.time() - start_time)) + '\n')

		if VIDEO:
			video.release()


	""" Determine if the centroid count in each quadrant passes """
	def checkImage(self,isSmallBB,quad1_cnt,quad2_cnt,quad3_cnt):

		if isSmallBB:
			return self.checkSmallBB(quad1_cnt,quad2_cnt,quad3_cnt)
		else:
			return self.checkLargeBB(quad1_cnt,quad2_cnt,quad3_cnt)

	""" Check to see if the image passes with the large BB size """
	def checkLargeBB(self,quad1_cnt,quad2_cnt,quad3_cnt):

		if ((quad1_cnt>0) and (quad2_cnt > 0) and (quad3_cnt>0)):
			return True
		return False

	""" Check to see if the image passes with the Small BB size """
	def checkSmallBB(self,quad1_cnt,quad2_cnt,quad3_cnt):	

		if ((quad1_cnt>0) and (quad2_cnt == 0) and (quad3_cnt>0)):
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
	def inspectImageFromCamera(self, isSmallBB, inspectingUp):

		imagePasses = False
		ret, self.frame = self.capture.read()

		if IMAGE_CAPTURE:
			self.frame1 = self.frame.copy()
			self.frame2 = self.frame.copy()
			self.frame3 = self.frame.copy()

		""" Update the location of the ball bearing """
		#self.findBallBearing(self.frame.copy())

		""" Update the box locations based on the ball bearing location """
		self.current_calib.updateShapeLocations(self.ball_bearing_x, self.ball_bearing_y)

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

			""" Check if the shape is near the ball bearing """
			hyp = math.sqrt(((cX - self.ball_bearing_x)**2) + ((cY - self.ball_bearing_y)**2))
			if (hyp < 260) and ((area == 0.000001) or (area > 20)):

				""" draw the contour and center of the shape on the image """
				cv2.drawContours(self.frame, [c], -1, (0, 255, 0), 2)
				cv2.circle(self.frame, (cX, cY), 7, (0, 0, 0), -1)

				if IMAGE_CAPTURE:
					cv2.drawContours(self.frame1, [c], -1, (0, 0, 255), 2)
					cv2.circle(self.frame1, (cX, cY), 7, (0, 0, 0), -1)
					cv2.drawContours(self.frame2, [c], -1, (0, 0, 255), 2)
					cv2.circle(self.frame2, (cX, cY), 7, (0, 0, 0), -1)
					cv2.drawContours(self.frame3, [c], -1, (0, 0, 255), 2)
					cv2.circle(self.frame3, (cX, cY), 7, (0, 0, 0), -1)


				""" Determine the number of centroids in each quadrant """
				if self.current_calib.inShape(1,cX,cY):
					quad1_cnt += 1
				elif self.current_calib.inShape(2,cX,cY):
					quad2_cnt += 1
				elif self.current_calib.inShape(3,cX,cY):
					quad3_cnt += 1

		""" Draw the Boxes around each of the areas """
		self.current_calib.drawShapes(self.frame)

		""" Show current circle """
		cv2.circle(self.frame, (self.ball_bearing_x, self.ball_bearing_y), self.current_calib.radius, (255, 0, 0), 2)

		""" Determine if the ball bearing case sizes pass """
		imagePasses = self.checkImage(isSmallBB,quad1_cnt,quad2_cnt,quad3_cnt)

		if IMAGE_CAPTURE:
			self.current_calib.drawShapes(self.frame3)
			cv2.circle(self.frame2, (self.ball_bearing_x, self.ball_bearing_y), self.current_calib.radius, (255, 0, 0), 2)
			cv2.circle(self.frame3, (self.ball_bearing_x, self.ball_bearing_y), self.current_calib.radius, (255, 0, 0), 2)
			cv2.putText(self.frame3, "Inspection Passes: " + str(imagePasses), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.upper_green, 2)


		""" Indicate Whether the image passes or fails """
		cv2.putText(self.frame, "Inspection Passes: " + str(imagePasses), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.upper_green, 2)

		return imagePasses


	""" Updates the ball bearing location based on where it currently is """
	def findBallBearing(self, frame):

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			
		""" Apply GuassianBlur to reduce noise. medianBlur is also added for smoothening, reducing noise """
		gray = cv2.GaussianBlur(gray,(1,1),100,100, 0);
		gray = cv2.medianBlur(gray,1)
			
		""" Adaptive Guassian Threshold is to detect sharp edges in the Image """
		gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,27,13.5)
			
		""" HoughCircles(image, method, dp, minDist[, circles[, param1[, param2 [, minRadius[, maxRadius]]]]]) """
		if RASP_PI:
                        circles = cv2.HoughCircles(gray, 3, 1, self.current_calib.circles_param, param1=30, param2=25, minRadius=40, maxRadius=0)
                else:
                        circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, self.current_calib.circles_param, param1=30, param2=25, minRadius=40, maxRadius=0)

			
		if circles is not None:
			""" convert the (x, y) coordinates and radius of the circles to integers """
			circles = np.round(circles[0, :]).astype("int")

			for (x, y, r) in circles:
				if self.current_calib.checkCircle(x,y,r):

					""" Adjust the ball position based on the received values """
					if(x != self.ball_bearing_x):
						self.ball_bearing_x = ((WEIGHT) * self.ball_bearing_x + x)/(WEIGHT+1) 
					if(y != self.ball_bearing_y):
						self.ball_bearing_y = ((WEIGHT) * self.ball_bearing_y + y)/(WEIGHT+1) 


	def testBB(self,position):

		""" Set the correct calibration """
		self.setCalibration(position)

		""" Initialize the ball bearing position """
		x_pos = self.current_calib.x_init
		y_pos = self.current_calib.x_init

		if VIDEO:
			video = cv2.VideoWriter('output.avi',-1, 7, (640,480))

		pic_count = 0
		start_time = time.time()

		while(True):
 
			pic_count += 1
			ret, frame = self.capture.read()	
			output = frame.copy()
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			
			""" Apply GuassianBlur to reduce noise. medianBlur is also added for smoothening, reducing noise """
			gray = cv2.GaussianBlur(gray,(1,1),100,100, 0);
			gray = cv2.medianBlur(gray,1)
			
			""" Adaptive Guassian Threshold is to detect sharp edges in the Image """
			gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,27,13.5)#29,15.5) working version
			

			""" HoughCircles(image, method, dp, minDist[, circles[, param1[, param2 [, minRadius[, maxRadius]]]]]) """
			circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 
				self.current_calib.circles_param, param1=30, param2=25, minRadius=40, maxRadius=0)
			
			if circles is not None:
				""" convert the (x, y) coordinates and radius of the circles to integers """
				circles = np.round(circles[0, :]).astype("int")

				for (x, y, r) in circles:

					if self.current_calib.checkCircle(x,y,r):
							
						self.my_print("x: " + str(x) + '\n')
						self.my_print("y: " + str(y) + '\n')				
						self.my_print("Radius is: " + str(r) + '\n')

						""" Adjust the ball position based on the received values """
						if(x != x_pos):
							x_pos = ((WEIGHT) * x_pos + x)/(WEIGHT+1) 
						if(y != y_pos):
							y_pos = ((WEIGHT) * y_pos + y)/(WEIGHT+1) 

			""" Show current circle """
			cv2.circle(output, (x_pos, y_pos), self.current_calib.radius, (255, 0, 0), 4)

			if VIDEO:
				video.write(output) 

			""" Display the resulting frame """
			cv2.imshow('frame',output)
		 	if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		end_time = time.time()
		elapsed_time = end_time - start_time
		print "number of frames: " + str(pic_count)
		print "elapsed time: " + str(elapsed_time)
		print "fps: " 
		print pic_count/elapsed_time

		if VIDEO:
			video.release()
		self.capture.release()
		cv2.destroyAllWindows()


	""" Function to handle system prints """
	def my_print(self, text):
	    sys.stdout.write(str(text))
	    sys.stdout.flush()

	def imageCapture(self):

		image_count = 0

		while(True):

			ret, self.frame = self.capture.read()
			cv2.imshow('Inspected Camera Image ', self.frame)

			key = cv2.waitKey(1) & 0xFF
			if key == ord('q'):
				break
			elif key == ord('s'):

				image_count += 1
				img = self.frame
				cv2.imwrite("../pictures/BlankPic_" + str(image_count) +".png", img) 



""" Used for testing purposes """
if __name__ == "__main__":

        blisk_num = 1
        stage_num = 0
        blade_num = 0
	blade_side = 0
	ball_bearing = 0 # 0 = large
	distance = 0
	pos = InspectionPosition.InspectionPosition()
	pos.setPos(blisk_num, stage_num, blade_num, blade_side, ball_bearing, distance)

	ip = ImageProcessor()
	if RASP_PI:
		ip.newBlisk(0)

	ip.inspect(None, pos)
	#ip.imageCapture()

		
