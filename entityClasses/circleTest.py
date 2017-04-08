# import the necessary packages
import numpy as np
import argparse
import cv2
import time
import sys

cap = cv2.VideoCapture(1) # Set Capture Device, in case of a USB Webcam try 1, or give -1 to get a list of available devices

#Set Width and Height 
# cap.set(3,1280)
# cap.set(4,720)

# The above step is to set the Resolution of the Video. The default is 640x480.
# This example works with a Resolution of 640x480.

""" Function to handle system prints """
def my_print(text):
    sys.stdout.write(str(text))
    sys.stdout.flush()





Y_MAX = 200
Y_MIN = 130
X_MAX = 420
X_MIN = 300
MIN_RAD_SMALL = 50
MAX_RAD_SMALL = 70 
MIN_RAD_LARGE = 70
MAX_RAD_LARGE = 80
WEIGHT = 7 

def test3(isSmallBB):

	x_pos = 370
	y_pos = 156

	w=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ))
	h=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ))

	print w
	print h

	capSize = (w,h)#(640, 480) # this is the size of my source video
	fourcc = cv2.cv.CV_FOURCC(*'XVID') #'W', 'M', 'V', '2')
	video = cv2.VideoWriter('output.avi',-1, 7, capSize)
	#video.write(125 * np.ones((100,100,3), np.uint8)) 

	pic_count = 0
	start_time = time.time()

	while(True):

		# Capture frame-by-frame
		ret, frame = cap.read()

		pic_count += 1
				
		output = frame.copy()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		# apply GuassianBlur to reduce noise. medianBlur is also added for smoothening, reducing noise.
		gray = cv2.GaussianBlur(gray,(1,1),100,100, 0);
		gray = cv2.medianBlur(gray,1)
		
		# Adaptive Guassian Threshold is to detect sharp edges in the Image. For more information Google it. # 11 3.5
		gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,27,13.5)#29,15.5) working version
		
		
		# detect circles in the image
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



""" For testing purposes """
if __name__=="__main__":


	test3(False)
