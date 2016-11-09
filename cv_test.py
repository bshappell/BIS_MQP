
import numpy as np
import cv2
import LED

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

if __name__=="__main__":

	#simpleImage()
	#catPic()
	#camTest()
	captureImage()
