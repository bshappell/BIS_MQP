

# ToolSwitch Class
import RPi.GPIO as GPIO
import time
import pigpio

LARGE_DC = 8.2
SMALL_DC = 3.0

WIRING_PI = False

if WIRING_PI:
        import wiringpi

SMALL_BB = 0
LARGE_BB = 1

""" 0-255 pwm to control Servo turns it, electromagnets holds it in place, two different electromagnets, high signal to turn """
class ToolSwitch(object):

	def __init__(self, servoPowerPin, servoSignalPin):

		""" Set up the servo class """
		self.servo = Servo(servoPowerPin, servoSignalPin)

		""" current state """
		self.state = None
		self.smallBB()

	""" Switch to the Small Ball Bearing """
	def smallBB(self):
                print "Switching to Small"
                if(self.state == SMALL_BB):
                        return

                """ Use the servo to switch tools """
                self.servo.switchToSmallBB()
                self.state = SMALL_BB

	""" Switch to the Large ball bearing """
	def largeBB(self):
                print "Switching to Large"
                if(self.state == LARGE_BB):
                        return

                """ Use the servo to switch tools """
                self.servo.switchToLargeBB()
                self.state = LARGE_BB
                        

""" Class for the servo """
class Servo(object):

        def __init__(self, powerPin, signalPin):

                """ Save the pin values """
                self.powerPin = powerPin
                self.signalPin = signalPin

		GPIO.setmode(GPIO.BCM) # specify naming convention to use
		GPIO.setwarnings(False) # discard GPIO warnings
		GPIO.setup(self.powerPin,GPIO.OUT)
		GPIO.setup(self.signalPin, GPIO.OUT)

		self.pwm = GPIO.PWM(self.signalPin, 50) # 50Hz
		self.pwm.start(2.5)

		""" Turn off power to the servo """
                GPIO.output(self.powerPin, GPIO.LOW)
		

	def switchToSmallBB(self):

                """ Send power to the servo """
                GPIO.output(self.powerPin, GPIO.HIGH)

                """ Send the signal to move to the small BB position """
                self.pwm.ChangeDutyCycle(SMALL_DC)
                time.sleep(2)

                """ Turn off power to the servo """
                GPIO.output(self.powerPin, GPIO.LOW)


        def switchToLargeBB(self):

                """ Send power to the servo """
                GPIO.output(self.powerPin, GPIO.HIGH)
                time.sleep(0.1)

                """ Send the signal to move to the large BB position """
                self.pwm.ChangeDutyCycle(LARGE_DC)
                time.sleep(2)

                """ Turn off power to the servo """
                GPIO.output(self.powerPin, GPIO.LOW)

        def testRun(self, val):

                """ Send power to the servo """
                GPIO.output(self.powerPin, GPIO.HIGH)
                time.sleep(0.1)

                """ Send the signal to move to the large BB position """
                if WIRING_PI:
                        wiringpi.pwmWrite(self.signalPin, val)
                        time.sleep(1)
                else:
                        self.pwm.start(7.5)
                        time.sleep(1)
                        for i in range(5):
                                self.pwm.ChangeDutyCycle(6)
                                print str(7.5) + "% duty cycle"
                                time.sleep(1)

                                self.pwm.ChangeDutyCycle(11)
                                print str(12.5) + "% duty cycle"
                                time.sleep(1)

                """ Turn off power to the servo """
                time.sleep(0.1)
                GPIO.output(self.powerPin, GPIO.LOW)

                self.close()

        def close(self):

                self.pwm.stop()
                GPIO.cleanup()
                


""" Used for testing purposes """
if __name__ == "__main__":

	""" Test switching between the different ball bearing sizes """
	toolSwitch = ToolSwitch(17,4)
	#toolSwitch.testRun(2)

        print "Swtich to small bb"
        toolSwitch.smallBB()

        time.sleep(2)
   
        print "switch to large bb"
        toolSwitch.largeBB()

        time.sleep(2)
        print "Swtich to small bb"
        toolSwitch.smallBB()

        time.sleep(2)
   
        print "switch to large bb"
        toolSwitch.largeBB()

        time.sleep(2)
                
	
