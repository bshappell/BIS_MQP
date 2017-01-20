import LED
import ForceSensor
import ToolSwitch
import TurnTable
import Blisk
import CircuitCompletor
import ABBRobot
import ImageProcessor

# BIS (Blisk Inspection System) Class

# Define the Rasp Pinout
PIN_LED = 1
PIN_CLK = 2
PIN_DOUT = 3
PIN_DIN = 4
PIN_CS = 5
PIN_TOOL_SWITCH = 6
PIN_MOTOR_STEP = 7
PIN_MOTOR_DIR = 8
PIN_CC = 9


class BIS(object):

	def __init__(self):

		

		""" TODO: How to store inspection results? """


		""" Store current position for inspection """
		self.currBB = 0 # 0 indicates the small BB 1 indicates large BB
		self.currBlisk = None
		self.currStage = None

		""" Array to store blisks """
		self.blisks = []

		""" set up an LED """
		self.led = LED.LED(PIN_LED)

		""" set up the force sensor """
		self.forceSensor = ForceSensor.ForceSensor(PIN_CLK, PIN_DOUT, PIN_DIN, PIN_CS)

		""" set up the tool switch """
		self.toolSwitch = ToolSwitch.ToolSwitch(PIN_TOOL_SWITCH)

		""" set up the turntable stepper motor """
		self.turntable = TurnTable.TurnTable(PIN_MOTOR_STEP, PIN_MOTOR_DIR)

		""" set up the circuit completor """
		self.circuitCompletor = CircuitCompletor.CircuitCompletor(PIN_CC)

		""" set up the ABB Robot """
		self.abbRobot = ABBRobot.ABBRobot()

		""" set up the ImageProcessor class """
		self.imageProcessor = ImageProcessor.ImageProcessor()


	""" Selects the blisk that will be used for inspection """
	def selectBlisk(self, currBlisk):

		self.currBlisk = self.blisks[currBlisk]

	""" Position the arm far from the turntable for the current blisk """
	def positionArmFar(self):

		self.abbRobot.positionArmFar(currBlisk)

	""" Position the arm in between the blades of the current blisk """
	def positionArmClose(self):

		self.abbRobot.positionArmClose(currBlisk)

	""" Position the blisk on the turntable by turning until contact is made """
	def positionBlisk(self):

		""" Increment the stepper motor until contact is made with the arm """
		while(not self.circuitCompletor.getContact()):

			self.turntable.increment()

	""" Start the inspection of the current blisk """
	def inspectBlisk(self):

		""" turn on the LED for inspection """
		self.led.turnOn()

		""" Begin sending the force sensing readings to the abb robot """
		

		""" Use the small BB size first """
		self.abbRobot.pullArmBack()
		self.currBB = 0
		self.toolSwitch.smallBB()

		""" Inspect the blisk with both BB sizes """
		for i in range(2):

			""" Inspect all Stages of the blisk """
			for stage in self.currBlisk.stages:

				""" Increment over every blade """
				for blade in range(self.stage.numberBlades):

					""" Inspect the blade """
					self.inspectBlade()

					""" Increment the turntable by one blade """
					self.turntable.incrementBlade(currStage)

			""" Switch to the larger BB size """
			self.currBB = 1
			self.abbRobot.pullArmBack()
			self.toolSwitch.largeBB()

		""" Turn off the led when the inspection is complete """
		self.led.turnOff()
	

