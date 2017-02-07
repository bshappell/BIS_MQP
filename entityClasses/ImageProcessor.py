# ImageProcessor Class
import cv2

class ImageProcessor(object):

	def __init__(self):

		self.capture = cv2.VideoCapture(0)

	def inspectImage(self, currStage, sizeBB):

		""" Capture frame-by-frame """
                ret, frame = cap.read()

                cv2.imshow('frame',frame)

    """ When everything done, release the capture """
	def shutdown(self):
		self.capture.release()
		cv2.destroyAllWindows()
		self.capture.release()
