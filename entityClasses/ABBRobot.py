# ABBRobot Class
import Blisk
import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

""" BLISK IDS """
BLISK_1 = 0x01
BLISK_2 = 0x02
BLISK_3 = 0x03

""" STAGE NUMBER """
STAGE_1 = 0x01
STAGE_2 = 0x02

""" MESSAGE TYPES """
MT_CHECK_CONNECTION = 0x00
MT_ARM_HOME = 0x01
MT_ARM_FAR = 0x02
MT_ARM_CLOSE = 0x03
MT_INSPECT_BLADE = 0x04
MT_FORCE_MEASUREMENT = 0x05
MT_POS_UPDATE = 0x06
MT_MOVEMENT_COMPLETE = 0x07
MT_CONNECTION_GOOD = 0x08

class ABBRobot(object):

	def __init__(self):

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

	""" Used to test sending packets """
	def sendPacket(self):

		self.socket.sendto(MESSAGE, (UDP_IP, UDP_PORT))


	""" Check that the arm is up and running, and the connection between the Pi and IRC5 is good """
	def checkConnection(self):

		pass

	""" position the arm for inspection for the current blisk """
	def positionArmFar(self, currBlisk):

		""" Message Format: (MT_ARM_FAR, BLISK_X, STAGE_X) """

		pass

	""" position the arm for inspection for the current blisk """
	def positionArmClose(self, currBlisk):

		""" Message Format: (MT_ARM_CLOSE, BLISK_X, STAGE_X) """

		pass

	""" Positon the arm in the center of the current blade """
	def inspectBlade(self, currBlisk, currStage):

		""" Message Format: (MT_INSPECT_BLADE, BLISK_X, STAGE_X) """

		pass

	""" Move the arm back away from the blisk for the placing and removing of the blisk """
	def pullArmBack(self):

		""" Message Format: (MT_ARM_HOME, BLISK_X, STAGE_X) """

		pass

	""" Send the current force sensing measurement to the controller """
	def sendForceMeasurement(self, measurement):

		""" Message Format: (MT_FORCE_MEASUREMENT, measurement) """

		pass

	""" Handle a message received from the IRC5 controller """
	def handleMessage(self):

		pass


""" Used for testing purposes """
if __name__ == "__main__":

	abb = ABBRobot()

	for i in range(100):

		abb.sendPacket()
		time.sleep(0.5)