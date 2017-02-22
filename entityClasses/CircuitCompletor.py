# CircuitCompletor Class
import RPi.GPIO as GPIO
import time

class CircuitCompletor(object):

	def __init__(self, pinNumber):

		""" set the pinNumber """
		self.pinNumber = pinNumber

		""" set up the GPIO pin specified """
		GPIO.setmode(GPIO.BCM) # specify naming convention to use
		GPIO.setwarnings(False) # discard GPIO warnings
		GPIO.setup(self.pinNumber, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	def getContact(self):

		reading = GPIO.input(self.pinNumber)
		#print(reading)
		return reading
	

""" Used for testing purposes """
if __name__ == "__main__":

        """ for CircuitCompletor testing purposes """
        cc = CircuitCompletor(12)
        t = 0
        while(t < 30):
	        cc.getContact
	        time.sleep(1)
	        cc.getContact
	        t += 1
