# LED Class 
import RPi.GPIO as GPIO
import time

""" TODO: use PWM instead """
class LED(object):

	""" An LED that is part of the Blisk Inspection System.
	LEDs have the following attributes:

	pinNumber: The pin nummber on the Rasp Pi that the LED is connected to.
	"""

	def __init__(self, pinNumber):

		""" set the pinNumber """
		self.pinNumber = pinNumber

		""" set up the GPIO pin specified """
		GPIO.setmode(GPIO.BCM) # specify naming convention to use
		GPIO.setwarnings(False) # discard GPIO warnings
		GPIO.setup(pinNumber,GPIO.OUT) # set the pin as an output

	def turnOn(self):

		""" code to turn the rasp pi pin on """
		GPIO.output(self.pinNumber, GPIO.HIGH)

	def turnOff(self):

		""" code to turn the rasp pi pin off """
		GPIO.output(self.pinNumber, GPIO.LOW)


""" Used for testing purposes """
if __name__ == "__main__":

        """ for LED testing purposes """
        led = LED(12)
        led.turnOn()
        time.sleep(5)
        led.turnOff()
        
