
import numpy as np
import cv2
#import LED

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
	led = LED.LED(12)
	led.turnOn()
	cap = cv2.VideoCapture(0)
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

	led.turnOff()


def detectCircle():

	img_filt = cv2.medianBlur(cv2.imread('pictures\\capture5.png',0), 5)
	img_th = cv2.adaptiveThreshold(img_filt,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	contours, hierarchy = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	#cnt = contours[4]
	#cv2.drawContours(img_th, [cnt], 0, (0,255,0), 3)
	#cv2.drawContours(img_th, contours, -1, (0,255,0), 3)

	"""im = cv2.imread('pictures\\testPic.png')
	imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(imgray,127,255,0)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)"""

	imageCount = 0 # used to increment picture counts

	while 1:

		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			break
		# Save the Image if we receive an s key press
		elif key == ord('s'):
			imageCount += 1 # increment the image count variable
			cv2.imwrite('img_threshold' + str(imageCount) + '.png',img_th)

		cv2.imshow('filt', img_th)


if __name__=="__main__":

	#simpleImage()
	#catPic()
	#camTest()
	#captureImage()
	detectCircle()
