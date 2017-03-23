import LED
import ForceSensor
import ToolSwitch
import TurnTable
import Blisk
import CircuitCompletor
import ABBRobot
import Stage
import ImageProcessor
import time
import sys

# BIS (Blisk Inspection System) Class

# Define the Rasp Pinout
PIN_MOTOR_STEP = 20 # Stepper Motor Step Signal
PIN_MOTOR_DIR = 16 # Stepper Motor Direction Signal
PIN_SERVO_SIG = 4 # Tool Switch Servo Signal
PIN_SERVO_POWER = 17 # Tool Switch Power Signal
PIN_LED_SIG = 22 # LED Signal
PIN_CC = 5 # Circuit Completor Pin
PIN_FS_DATA = 24 # Force Sensor Data Pin
PIN_FS_CLK = 23 # Force Sensor Clock Pin

""" Define the different inspection times for each blisk """
IT_BLISK_P01 = 10
IT_BLISK_P02 = 10
IT_BLISK_G02 = 20

""" Number of Blades per Stage """
BN_STAGE_P01 = 56
BN_STAGE_P02 = 34
BN_STAGE_G02_1 = 49
BN_STAGE_G02_2 = 39

""" The Blisk IDs """
ID_BLISK_P01 = '2468M19P01'
ID_BLISK_P02 = '2468M17P02'
ID_BLISK_G02 = '2468M18G02'


class BIS(object):

	def __init__(self):

		""" TODO: How to store inspection results? """


		""" Store current position for inspection """
		self.currBB = 0 # 0 indicates the small BB 1 indicates large BB
		self.currBlisk = None
		self.currStage = 0
		self.currBlade = 0
		self.bliskNum = None

		""" The arrays of steps between blades for the different stages """
		# TODO add error accounting to step arrays
		stepsArray_P01 = [600]*56
		stepsArray_P02 = [988]*34
		stepsArray_G02_1 = [686]*49
		stepsArray_G02_2 = [861]*39

		""" Make the different stages Stage(numberBlades, smallBBRadius, largeBBRadius, stepsArray) """
		stage_P01 = [Stage.Stage(56, 0.05, 0.07, stepsArray_P01)]
		stage_G02 = [Stage.Stage(49, 0.09, 0.11, stepsArray_G02_1), Stage.Stage(39, 0.105, 0.125, stepsArray_G02_2)]
		stage_P02 = [Stage.Stage(34, 0.122, 0.142, stepsArray_P02)]

		""" The Blisks composed of the different stages Blisk(bliskID, inspectionTime, firstStage, secondStage) """
		blisk_P01 = Blisk.Blisk(ID_BLISK_P01, IT_BLISK_P01, stage_P01)
		blisk_P02 = Blisk.Blisk(ID_BLISK_P02, IT_BLISK_P02, stage_P02)
		blisk_G02 = Blisk.Blisk(ID_BLISK_G02, IT_BLISK_G02, stage_G02)

		""" Array to store blisks """
		self.blisks = [blisk_P01, blisk_P02, blisk_G02]

		""" set up an LED """
		self.led = LED.LED(PIN_LED_SIG)

		""" set up the ABB Robot """
		self.abbRobot = ABBRobot.ABBRobot()

		""" set up the force sensor """
		self.forceSensor = ForceSensor.ForceSensor(PIN_FS_DATA, PIN_FS_CLK, self.abbRobot.sendForceMeasurement)

		""" set up the tool switch """
                self.toolSwitch = ToolSwitch.ToolSwitch(PIN_SERVO_POWER, PIN_SERVO_SIG)

		""" set up the turntable stepper motor """
		self.turntable = TurnTable.TurnTable(PIN_MOTOR_STEP, PIN_MOTOR_DIR)

		""" set up the circuit completor """
		self.circuitCompletor = CircuitCompletor.CircuitCompletor(PIN_CC)

		""" set up the ImageProcessor class """
		self.imageProcessor = ImageProcessor.ImageProcessor()

		""" set up the force sensor class """
		self.forceSensor = ForceSensor.ForceSensor(PIN_FS_DATA, PIN_FS_CLK, self.abbRobot.sendForceMeasurement)

	""" Handles the startup of the BIS """
	def start(self):

		""" Check the connection with the ABB Robot """
		if(self.abbRobot.checkConnection()):
			print "Connection with abb robot successful"
		else:
			print "Connection failed"

		""" Home the Abb Robot arm """
		self.abbRobot.pullArmBack()


	""" Selects the blisk that will be used for inspection """
	def selectBlisk(self, currBlisk):

		""" Check that the blisk number is either 0,1,2 """
		if(currBlisk > 2 or currBlisk < 0):
			print "ERROR INCORRECT BLISK NUMBER RECIEVED"
			return

                self.bliskNum = currBlisk
		self.currBlisk = self.blisks[currBlisk]

	""" Position the arm far from the turntable for the current blisk """
	def positionArmFar(self):

		if(not self.abbRobot.positionArmFar(self.bliskNum)):
			print "ERROR POSITIONING THE ARM FAR - in positionArmFar"
			return

		""" Check that there is no contact with the blisk and zero the Force Sensor """
		if(self.circuitCompletor.getContact()):
			print "ERROR CONTACT WITH BLISK DETECTED"
			return

                """ set up the force sensor """
		self.forceSensor.zeroSensor()

		""" Use the small BB size first """
		self.abbRobot.pullArmBack()
		self.currBB = 0
		self.toolSwitch.smallBB()
		

	""" Position the arm in between the blades of the current blisk """
	def positionArmClose(self):

		if(not self.abbRobot.positionArmClose(self.bliskNum)):
                        return


	""" Position the blisk on the turntable by turning until contact is made """
	def positionBlisk(self):

		""" Increment the stepper motor until contact is made with the arm """
		# TODO make sure that it doesnt turn more than one blade rotation
		print "turning blisk until contact is made"
		while(not self.circuitCompletor.getContact()):

			self.turntable.increment(0)
			time.sleep(0.002)
		print "contact made turning complete"

	""" Positions the arm for inspection by using force sensing """
	def positionArmForInspection(self):

                """ Begin sending the force sensing readings to the abb robot """
		#self.forceSensor.startReadings()

                pass

	""" Start the inspection of the current blisk """
	def inspectBlisk(self):

                self.positionArmForInspection()

		""" turn on the LED for inspection """
		self.led.turnOn()

		

		###### self.abbRobot.inspectBlade(self.bliskNum, 0)   #for testing purposes

		""" Inspect all Stages of the blisk """
		self.currStage = 0
		for stage in self.currBlisk.stages:

			print "Inspecting Stage"

			""" Use the small BB size first """
			#self.abbRobot.pullArmBack()
			#self.currBB = 0
			#self.toolSwitch.smallBB()

			""" Inspect the blisk with both BB sizes """
			for i in range(2):

				#print "Switch BB size"

				""" Increment over every blade """
				for blade in range(stage.numberBlades):

					print "inspect blade: " + str(blade)

					""" Set the current blade """
					self.currBlade = blade

					""" Position Arm for Inspection """
					#self.abbRobot.posArmForInspection(self.currBlisk, stage)

					""" Inspect the blade """
					self.inspectBlade()

					""" Increment the turntable by one blade """
					self.turntable.incrementBlade(stage, blade)

					time.sleep(1)

				""" Switch to the larger BB size """
				self.currBB = 1
				self.abbRobot.pullArmBack()
				self.toolSwitch.largeBB()

			self.abbRobot.positionArmClose(self.currBlisk)

			""" switch to the second stage """
			self.currStage = 1

		""" Turn off the led when the inspection is complete """
		self.led.turnOff()

		""" Stop sending the force sensing readings """

		print "Blisk Inspection Function Complete"

	""" Handle the inspection of the current blade """
	def inspectBlade(self):

		self.abbRobot.inspectBlade(self.bliskNum, self.stageNum)  

		while(self.abbRobot.inspecting(self.bliskNum, self.stageNum)):
                        
                        self.imageProcessor.inspect(True)
		

	""" Handle quitting and shutting down the system """
	def shutdown(self):

                 self.forceSensor.end()
                 self.abbRobot.closeComm()
                 self.led.turnOff()
                 self.imageProcessor.shutdown()

	
""" Run the Blisk Application """
if __name__ == "__main__":

        bis = BIS()
        











        
