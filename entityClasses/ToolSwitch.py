

# ToolSwitch Class
import RPi.GPIO as GPIO
import time


""" 0-255 pwm to control Servo turns it, electromagnets holds it in place, two different electromagnets, high signal to turn """
class ToolSwitch(object):

	def __init__(self, servoPin, em1_s1, em1_s2, em2_s1, em2_s2):

		""" set the pin numbers """
		self.servoPin = servoPin

		""" Set up the Electromagnets """
		self.em1 = Electromagnet(em1_s1, em1_s2)
		self.em2 = Electromagnet(em2_s1, em2_s2)

		""" set up the pins as outputs """
		GPIO.setmode(GPIO.BCM) # specify naming convention to use
		GPIO.setwarnings(False) # discard GPIO warnings
		GPIO.setup(servoPin,GPIO.OUT) # set the pin as an output

	""" Function to comtrol running the servo """
	def runServo(self):

		# TO DO add servo functionality!!!!
		pass

	""" Switch to the Small Ball Bearing """
	def smallBB(self):

		""" Turn off the electromagnet to unlock the tool """
		#self.em1.turnOff()
		#self.em2.turnOn()

		""" Use the servo to switch tools """
		self.runServo()

		""" Use the other electromagnet to lock the tool in place """
		#self.em1.turnOff()
		#self.em2.turnOn()

	""" Switch to the Large ball bearing """
	def largeBB(self):

		""" Turn off the electromagnet to unlock the tool """
		#self.em1.turnOff()
		#self.em2.turnOn()

		""" Use the servo to switch tools """
		self.runServo()

		""" Use the other electromagnet to lock the tool in place """
		#self.em1.turnOff()
		#self.em2.turnOn()


""" Class for Electromagnet """
class Electromagnet(object):

	def __init__(self, s1, s2):

		""" Store the pin numbers """
		self.s1 = s1
		self.s2 = s2

		""" Set the pins as outputs """
		GPIO.setmode(GPIO.BCM) # specify naming convention to use
		GPIO.setwarnings(False) # discard GPIO warnings
		GPIO.setup(self.s1,GPIO.OUT) 
		GPIO.setup(self.s2,GPIO.OUT) 

	""" Function to turn on the electromagnet """
	def turnOn(self):

		# TODO Add turn on functionality
		pass

	""" Function to turn off the electromagnet """
	def turnOff(self):

		# TODO add turn off functionality
		pass
		

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
