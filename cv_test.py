
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
			cX = 0
			cY = 0
		else:
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
	 
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


if __name__=="__main__":

	detectSWs()
