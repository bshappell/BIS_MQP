# ImageProcessor Class
import cv2
import numpy as np
import InspectionResults
import InspectionPosition
import sys
import time
import Shapes

DEBUG = 0 # Toggle to get debug features
RASP_PI = 0 # Indicates whether the code is running on the Raspberry Pi or not
CAMERA = 1 # Indicates whether to run the code with the camera
VIDEO = 0 # Indicates if a video should be recorded

HUE_LOW = 26
HUE_HIGH = 71
SATURATION_LOW = 105
SATURATION_HIGH = 255
VALUE_LOW = 116 #116
VALUE_HIGH = 255

Y_MAX = 200
Y_MIN = 130
X_MAX = 420
X_MIN = 300
MIN_RAD_SMALL = 50
MAX_RAD_SMALL = 70 
MIN_RAD_LARGE = 70
MAX_RAD_LARGE = 80
WEIGHT = 7 

""" Per blade side and bb size per stage (16 in total) """
class CvCalibData(object):

	def __init__(self, radius, radius_max, radius_min, x_init, y_init, y_max, y_min, x_max, x_min):

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

	def update(self, radius, radius_max, radius_min, x_init, y_init, y_max, y_min, x_max, x_min):

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
		self.box1 = Shapes.Box(400,85,70,70,True)
		self.box2 = Shapes.Box(285,50,100,50,True)
		self.box3 = Shapes.Box(220,140,70,70,True)
		

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

	def inspect(self, callFunction, position):

		stillInspecting = True
		pic_count = 0
		image_count = 1

		while(stillInspecting):

			stillInspecting, blade_side, distance = callFunction(position)
			if ((distance != -1) and (blade_side != -1)):
				position.update(blade_side,distance)

			""" Inspect the captured image """
			passValue = self.inspectImageFromCamera(position.ball_bearing)
			cv2.imshow('Inspected Camera Image ', self.frame)

			""" Save the inspection results to the file """
			self.results.addResult(position, passValue)

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

		image_count = 1
		while(True):

			""" Inspect the captured image """
			passValue = self.inspectImageFromCamera(False)
			#self.findBBCamera()

			cv2.imshow('Inspected Camera Image ',self.frame)
			key = cv2.waitKey(1) & 0xFF
			if key == ord('q'):
				break
			elif key == ord('s'):
				image_count += 1
				img = self.frame
				cv2.imwrite("../pictures/Capture_" + str(image_count) +".png", img)
		
		""" Close all windows currently open """
		self.shutdown()


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
	def inspectImageFromCamera(self, isSmallBB):

		imagePasses = False
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

		if(DEBUG):
			 """ Indicate Whether the image passes or fails """
			 cv2.putText(self.frame, "Inspection Passes: " + str(imagePasses), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.upper_green, 2)

		return imagePasses


	def test3(isSmallBB):

		x_pos = 370
		y_pos = 156

		if VIDEO:
			video = cv2.VideoWriter('output.avi',-1, 7, (640,480))

		pic_count = 0
		start_time = time.time()

		while(True):
 
			pic_count += 1
			ret, frame = cap.read()	
			output = frame.copy()
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			
			""" Apply GuassianBlur to reduce noise. medianBlur is also added for smoothening, reducing noise """
			gray = cv2.GaussianBlur(gray,(1,1),100,100, 0);
			gray = cv2.medianBlur(gray,1)
			
			""" Adaptive Guassian Threshold is to detect sharp edges in the Image """
			gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,27,13.5)#29,15.5) working version
			

			# cv2.HoughCircles(image, method, dp (was 5), minDist (260?)[, circles[, param1[, param2 (65?)[, minRadius[, maxRadius]]]]])
			if isSmallBB:
				circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 4, param1=30, param2=25, minRadius=40, maxRadius=0)
			else:
				circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 1, param1=30, param2=25, minRadius=40, maxRadius=0)
			
			# ensure at least some circles were found
			if circles is not None:
				# convert the (x, y) coordinates and radius of the circles to integers
				circles = np.round(circles[0, :]).astype("int")
				
				# loop over the (x, y) coordinates and radius of the circles
				for (x, y, r) in circles:
					# draw the circle in the output image, then draw a rectangle in the image
					# corresponding to the center of the circle
					#if(r > 70): (for larger bb)
					if isSmallBB:

						if(r > MIN_RAD_SMALL) and (r < MAX_RAD_SMALL) and (y<Y_MAX) and (y>Y_MIN) and (x<X_MAX) and (x>X_MIN): 
							cv2.circle(output, (x, y), r, (0, 255, 0), 4)
							cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
							#time.sleep(0.5)
							print "x: " + str(x)
							print "y: " + str(y)
							my_print("Radius is: ")
							my_print(r)
							my_print("\n")


					elif (r > MIN_RAD_LARGE) and (r < MAX_RAD_LARGE) and (y<Y_MAX) and (y>Y_MIN) and (x<X_MAX) and (x>X_MIN):
							
						#cv2.circle(output, (x, y), r, (0, 255, 0), 4)
						#cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
						#time.sleep(0.5)
						my_print("x: " + str(x) + '\n')
						my_print("y: " + str(y) + '\n')				
						my_print("Radius is: ")
						my_print(r)
						my_print("\n")

						""" Adjust the ball pos based on the received values """
						if(x != x_pos):
							x_pos = ((WEIGHT) * x_pos + x)/(WEIGHT+1) 
						if(y != y_pos):
							y_pos = ((WEIGHT) * y_pos + y)/(WEIGHT+1) 

			""" Show expected circle """
			if isSmallBB:
				cv2.circle(output, (370, 156), 64, (255, 0, 0), 4)
				#cv2.rectangle(output, (X_MIN - 80, Y_MIN - 50), (X_MAX + 80, Y_MAX + 50), (0, 128, 255), 1)
			else:
				#cv2.circle(output, (370, 156), 74, (255, 0, 0), 4)
				cv2.circle(output, (x_pos, y_pos), 74, (255, 0, 0), 4)
				#cv2.rectangle(output, (X_MIN - 80, Y_MIN - 50), (X_MAX + 80, Y_MAX + 50), (0, 128, 255), 1)


			video.write(output) #125 * np.ones((100,100,3), np.uint8)) 

			# Display the resulting frame
			#cv2.imshow('gray',gray)
			cv2.imshow('frame',output)
		 	if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		# When everything done, release the capture
		end_time = time.time()
		elapsed_time = end_time - start_time
		print "number of frames: " + str(pic_count)
		print "elapsed time: " + str(elapsed_time)
		print "fps: " 
		print pic_count/elapsed_time

		video.release()
		cap.release()
		cv2.destroyAllWindows()


	""" Function to handle system prints """
	def my_print(self, text):
	    sys.stdout.write(str(text))
	    sys.stdout.flush()




""" Used for testing purposes """
if __name__ == "__main__":

	ip = ImageProcessor()
	ip.inspectCameraImage()
	#ip.findBBCamera()
















		
