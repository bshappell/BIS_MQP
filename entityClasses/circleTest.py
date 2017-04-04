# import the necessary packages
import numpy as np
import argparse
import cv2
import time
import sys

cap = cv2.VideoCapture(0) # Set Capture Device, in case of a USB Webcam try 1, or give -1 to get a list of available devices

#Set Width and Height 
# cap.set(3,1280)
# cap.set(4,720)

# The above step is to set the Resolution of the Video. The default is 640x480.
# This example works with a Resolution of 640x480.

""" Function to handle system prints """
def my_print(text):
    sys.stdout.write(str(text))
    sys.stdout.flush()

def test1():

	while(True):

		# Capture frame-by-frame
		ret, frame = cap.read()

		# load the image, clone it for output, and then convert it to grayscale
				
		output = frame.copy()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		# apply GuassianBlur to reduce noise. medianBlur is also added for smoothening, reducing noise.
		gray = cv2.GaussianBlur(gray,(1,1),223,222, 0);
		gray = cv2.medianBlur(gray,9)
		
		# Adaptive Guassian Threshold is to detect sharp edges in the Image. For more information Google it. # 11 3.5
		gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,21,3.5)
		
		"""kernel = np.ones((2.6,2.7),np.uint8)
		gray = cv2.erode(gray,kernel,iterations = 1)
		# gray = erosion
		
		gray = cv2.dilate(gray,kernel,iterations = 1)"""
		# gray = dilation

		# get the size of the final image
		# img_size = gray.shape
		# print img_size
		
		# detect circles in the image
		circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 260, param1=30, param2=65, minRadius=0, maxRadius=0) # 40 100
		# print circles
		
		# ensure at least some circles were found
		if circles is not None:
			# convert the (x, y) coordinates and radius of the circles to integers
			circles = np.round(circles[0, :]).astype("int")
			
			# loop over the (x, y) coordinates and radius of the circles
			for (x, y, r) in circles:
				# draw the circle in the output image, then draw a rectangle in the image
				# corresponding to the center of the circle
				cv2.circle(output, (x, y), r, (0, 255, 0), 4)
				cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
				#time.sleep(0.5)
				"""print "Column Number: "
				print x
				print "Row Number: "
				print y"""
				my_print("Radius is: ")
				my_print(r)
				my_print("\n")

		# Display the resulting frame
			cv2.imshow('gray',gray)
	    	cv2.imshow('frame',output)
	 	if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

def test2(pic,isSmallBB):

	while(True):

		# Capture frame-by-frame
		#ret, frame = cap.read()
		#frame = cv2.imread('BIS_MQP\\pictures\\Plain_Large.png',0)
		frame = cv2.imread(pic,0)

		# load the image, clone it for output, and then convert it to grayscale
				
		output = frame.copy()
		gray = frame.copy() #cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		# apply GuassianBlur to reduce noise. medianBlur is also added for smoothening, reducing noise.
		gray = cv2.GaussianBlur(gray,(1,1),100,100, 0);
		gray = cv2.medianBlur(gray,1)
		
		# Adaptive Guassian Threshold is to detect sharp edges in the Image. For more information Google it. # 11 3.5
		gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,29,15.5)#29,18.5)
		
		"""kernel = np.ones((2.6,2.7),np.uint8)
		gray = cv2.erode(gray,kernel,iterations = 1)
		# gray = erosion
		
		gray = cv2.dilate(gray,kernel,iterations = 1)"""
		# gray = dilation

		# get the size of the final image
		# img_size = gray.shape
		# print img_size
		
		# detect circles in the image
		# cv2.HoughCircles(image, method, dp (was 5), minDist (260?)[, circles[, param1[, param2 (65?)[, minRadius[, maxRadius]]]]])
		circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 5, param1=30, param2=25, minRadius=40, maxRadius=0) # 40 100
		# print circles
		
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

					if(r > 50) and (r < 100): # for small bb
						cv2.circle(output, (x, y), r, (0, 255, 0), 4)
						cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
						#time.sleep(0.5)
						"""print "Column Number: "
						print x
						print "Row Number: "
						print y"""
						my_print("Radius is: ")
						my_print(r)
						my_print("\n")

				elif (r > 70) and (r < 100): # for small bb
						
					cv2.circle(output, (x, y), r, (0, 255, 0), 4)
					cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
					#time.sleep(0.5)
					"""print "Column Number: "
					print x
					print "Row Number: "
					print y"""
					my_print("Radius is: ")
					my_print(r)
					my_print("\n")

		# Display the resulting frame
			cv2.imshow('gray',gray)
	    	cv2.imshow('frame',output)
	 	if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()



""" For testing purposes """
if __name__=="__main__":

	test2('BIS_MQP\\pictures\\Plain_Large.png',False)
	test2('BIS_MQP\\pictures\\Plain_Small.png',True)