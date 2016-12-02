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

	""" Position the arm for the current blisk """
	def positionArm(self):

		self.abbRobot.positionArm(currBlisk)


	def positionBlisk(self):

		""" Increment the stepper motor until contact is made with the arm """
		while(not self.circuitCompletor.getContact):

			self.turntable.increment()

	def inspectBlisk(self):

		""" turn on the LED for inspection """
		self.led.turnOn()

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

					""" Center the robot arm in the blade """
					self.abbRobot.centerInBlade(currBlisk, stage)

					""" Inspect the top half of the blade """
					self.inspectBlade()

					""" Re center the robot arm in the blade """
					self.abbRobot.centerInBlade(currBlisk, stage)

					""" Inspect the bottom half of the blade """
					self.inspectBlade()

					""" Pull the arm back to be able to turn the blisk """
					self.abbRobot.pullArmBack()

					""" Increment the turntable by one blade """
					self.turntable.incrementBlade(currStage)

			""" Switch to the larger BB size """
			self.currBB = 1
			self.abbRobot.pullArmBack()
			self.toolSwitch.largeBB()

		""" Turn off the led when the inspection is complete """
		self.led.turnOff()


	""" Helper function to handle inspecting the blade from the center """
	def inspectBlade(self):

		""" Continue moving along the blade inspecting until the edge of the blade is reached """
		while(not self.circuitCompletor.getContact):

			""" Store the results from inspecting the image """
			self.imageProcessor.inspectImage(currStage, sizeBB)

		""" Stop the arm when the edge of the blade has been reached """
		self.abbRobot.stopBladeTraversal()
	

