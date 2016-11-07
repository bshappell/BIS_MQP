import LED
import ForceSensor
import ToolSwitch
import StepperMotor
import Blisk
import CircuitCompletor
import ABBRobot

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


		""" TODO way to store blisks """

		""" set up an LED """
		self.led = LED.LED(PIN_LED)

		""" set up the force sensor """
		self.forceSensor = ForceSensor.ForceSensor(PIN_CLK, PIN_DOUT, PIN_DIN, PIN_CS)

		""" set up the tool switch on pin 5 """
		self.toolSwitch = ToolSwitch.ToolSwitch(PIN_TOOL_SWITCH)

		""" set up the turntable stepper motor """
		self.stepperMotor = StepperMotor.StepperMotor(PIN_MOTOR_STEP, PIN_MOTOR_DIR)

		""" set up the circuit completor """
		self.circuitCompletor = CircuitCompletor.CircuitCompletor(PIN_CC)

		""" set up the ABB Robot """
		self.abbRobot = ABBRobot.ABBRobot()


	def selectBlisk(self):

		pass

	def positionArm(self):

		pass

	def positionBlisk(self):

		pass

	def inspectBlisk(self):

		pass