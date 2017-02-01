

# ToolSwitch Class
import RPi.GPIO as GPIO
import time


""" 0-255 pwm to control Servo turns it, electromagnets holds it in place, two different electromagnets, high signal to turn """
class ToolSwitch(object):

	def __init__(self, servoPin, electro1Pin, electro2Pin):

		""" set the pin numbers """
		self.servoPin = servoPin
		self.electro1Pin = electro1Pin
		self.electro2Pin = electro2Pin

		""" set up the pins as outputs """
		GPIO.setmode(GPIO.BCM) # specify naming convention to use
		GPIO.setwarnings(False) # discard GPIO warnings
		GPIO.setup(servoPin,GPIO.OUT) # set the pin as an output
		GPIO.setup(electro1Pin,GPIO.OUT) # set the pin as an output
		GPIO.setup(electro2Pin,GPIO.OUT) # set the pin as an output


        

	def smallBB(self):

		""" Turn off the electromagnet to unlock the tool """
		GPIO.output(self.electro1Pin, GPIO.LOW)
		GPIO.output(self.electro2Pin, GPIO.LOW)

		""" Use the servo to switch tools """

		""" Use the other electromagnet to lock the tool in place """
		GPIO.output(self.electro2Pin, GPIO.HIGH)

	def largeBB(self):

		""" Turn off the electromagnet to unlock the tool """
		GPIO.output(self.electro1Pin, GPIO.LOW)
		GPIO.output(self.electro2Pin, GPIO.LOW)

		""" Use the servo to switch tools """

		""" Use the other electromagnet to lock the tool in place """
		GPIO.output(self.electro1Pin, GPIO.HIGH)
		

""" Used for testing purposes """
if __name__ == "__main__":

	""" Test switching between the different ball bearing sizes """
	toolSwitch = ToolSwitch(14)
	time.sleep(5)
	toolSwitch.largeBB()
	time.sleep(5)
	toolSwitch.smallBB()
	time.sleep(5)
	toolSwitch.largeBB()
	time.sleep(5)
	toolSwitch.smallBB()
