

# ToolSwitch Class
import RPi.GPIO as GPIO
import time
import wiringpi

SMALL_BB = 0
LARGE_BB = 1

""" 0-255 pwm to control Servo turns it, electromagnets holds it in place, two different electromagnets, high signal to turn """
class ToolSwitch(object):

	def __init__(self, servoPowerPin, servoSignalPin, em1_s1, em1_s2, em2_s1, em2_s2):

		""" Set up the servo class """
		self.servo = Servo(servoPowerPin, servoSignalPin)

		""" Set up the Electromagnets """
		# self.em_small = Electromagnet(em1_s1, em1_s2)
		# self.em_large = Electromagnet(em2_s1, em2_s2)

		""" current state """
		self.state = None
		self.smallBB()

	""" Switch to the Small Ball Bearing """
	def smallBB(self):
                print "Switching to Small"
                if(self.state == SMALL_BB):
                        return

                """ Turn off the electromagnet to unlock the tool """
                # self.em_large.turnOff()

                """ Use the servo to switch tools """
                self.servo.switchToSmallBB()

                """ Use the other electromagnet to lock the tool in place """
                # self.em_small.turnOn()

                self.state = SMALL_BB

	""" Switch to the Large ball bearing """
	def largeBB(self):
                print "Switching to Large"
                if(self.state == LARGE_BB):
                        return

                """ Turn off the electromagnet to unlock the tool """
                # self.em_small.turnOff()

                """ Use the servo to switch tools """
                self.servo.switchToLargeBB()

                """ Use the other electromagnet to lock the tool in place """
                # self.em_large.turnOn()

                self.state = LARGE_BB
                        

""" Class for the servo """
class Servo(object):

        def __init__(self, powerPin, signalPin):

                """ Save the pin values """
                self.powerPin = powerPin
                self.signalPin = signalPin

                """ set up the pins as outputs """
		wiringpi.wiringPiSetupGpio()
		wiringpi.pinMode(self.signalPin, wiringpi.GPIO.PWM_OUTPUT)
		wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

		GPIO.setmode(GPIO.BCM) # specify naming convention to use
		GPIO.setwarnings(False) # discard GPIO warnings
		GPIO.setup(self.powerPin,GPIO.OUT)

		""" Turn off power to the servo """
                GPIO.output(self.powerPin, GPIO.LOW)
		
		""" Divide the pwm clock down """
		wiringpi.pwmSetClock(192)
		wiringpi.pwmSetRange(2000)

		self.delayPeriod = 5

	def switchToSmallBB(self):

                """ Send power to the servo """
                GPIO.output(self.powerPin, GPIO.HIGH)

                """ Send the signal to move to the small BB position """
                wiringpi.pwmWrite(self.signalPin, 95)
                time.sleep(self.delayPeriod)

                """ Turn off power to the servo """
                GPIO.output(self.powerPin, GPIO.LOW)


        def switchToLargeBB(self):

                """ Send power to the servo """
                GPIO.output(self.powerPin, GPIO.HIGH)

                """ Send the signal to move to the large BB position """
                wiringpi.pwmWrite(self.signalPin, 180)
                time.sleep(self.delayPeriod)

                """ Turn off power to the servo """
                GPIO.output(self.powerPin, GPIO.LOW)


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

		""" Set the EM to the zero position to avoid shoot-through """
		self.zero()
		time.sleep(0.05)

		""" Set the EM to the high position and hold until further notice """
		self.high()

	""" Function to turn off the electromagnet """
	def turnOff(self):

		""" Set the EM to the zero position briefly to avoid shoot-through """
		self.zero()
		time.sleep(0.05)

		""" Set the EM to the low position to release the magnet """
		self.low()
                time.sleep(1)

                """ Turn off the EM """
                self.zero()

	""" Function to send a +1 signal from the h-bridge by sending 1,0 """
	def high(self):

                GPIO.output(self.s1, GPIO.HIGH)
                GPIO.output(self.s2, GPIO.LOW)

        """ Function to send a 0 signal from the h-bridge by sending 0,0 """
	def zero(self):

                GPIO.output(self.s1, GPIO.LOW)
                GPIO.output(self.s2, GPIO.LOW)

        """ Function to send a -1 signal from the h-bridge by sending 0,1 """
	def low(self):

                GPIO.output(self.s1, GPIO.LOW)
                GPIO.output(self.s2, GPIO.HIGH)

""" Used for testing purposes """
if __name__ == "__main__":

	""" Test switching between the different ball bearing sizes """
	"""toolSwitch = ToolSwitch(18,27,5,6,13,19)
	time.sleep(5)
	toolSwitch.largeBB()
	time.sleep(5)
	toolSwitch.smallBB()
	time.sleep(5)
	toolSwitch.largeBB()
	time.sleep(5)
	toolSwitch.smallBB()"""

	servo = Servo(27,18)
	while(1):
                print "Swtich to small bb"
                servo.switchToSmallBB()
   
                print "switch to large bb"
                servo.switchToLargeBB()
                
	
