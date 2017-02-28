# ABBRobot Class
#import Blisk
import socket
import time
import sys

TCP_IP = "192.168.125.3" 
TCP_PORT = 5515
MESSAGE = "Hello, World!"

""" BLISK IDS """
BLISK_1 = 0x01
BLISK_2 = 0x02
BLISK_3 = 0x03

""" STAGE NUMBER """
STAGE_1 = 0x01
STAGE_2 = 0x02

# TODO Indicate which side

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
MT_INSPECTION_COMPLETE = 0x09

class ABBRobot(object):

	def __init__(self):

		""" Create a TCP/IP socket """
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		""" Bind the socket to the port """
		self.server_address = (TCP_IP, TCP_PORT)
		self.client_address = ""
		self.connection = None
		my_print('starting up on %s port %s\n' % self.server_address)
		self.socket.bind(self.server_address)

		""" Listen for incoming connections """
		self.socket.listen(1)


	""" Check that the arm is up and running, and the connection between the Pi and IRC5 is good """
	def checkConnection(self):
		self.my_print('waiting for a connection\n')
		self.connection, self.client_address = sock.accept()
		self.my_print('connection from ' + str(client_address))

		data = self.connection.recv(16)
		self.my_print('received "%s"\n' % data)

		""" Return whether the connection was successful of not """
		if data:
			self.my_print("received data from ABBRobot, connection good\n")
			return True 
		else:
			self.my_print("Did no recieve data from ABBRobot, connection failed\n")
			return False

	""" Position the arm for inspection for the current blisk """
	def positionArmFar(self, currBlisk):

		""" Message Format: (MT_ARM_FAR, BLISK_X, STAGE_X) """
		self.my_print('sending FAR to the client\n')
		self.connection.sendall("FAR")

		data = self.connection.recv(16)
		self.my_print('received "%s"\n' % data)

		if data == "FAR":
			self.my_print("received FAR from ABBRobot\n")
			return True 
		else:
			self.my_print("Did no recieve FAR from ABBRobot\n")
			return False

	""" Position the arm for inspection for the current blisk """
	def positionArmClose(self, currBlisk):

		""" Message Format: (MT_ARM_CLOSE, BLISK_X, STAGE_X) """
		self.my_print('sending NEAR to the client\n')
		self.connection.sendall("NEAR")

		data = self.connection.recv(16)
		self.my_print('received "%s"\n' % data)

		if data == "NEAR":
			self.my_print("received NEAR from ABBRobot\n")
			return True 
		else:
			self.my_print("Did no recieve NEAR from ABBRobot\n")
			return False

	""" Inspect the current blade """
	def inspectBlade(self, currBlisk, currStage):

		""" Message Format: (MT_INSPECT_BLADE, BLISK_X, STAGE_X) """
		self.my_print('sending INSPECT to the client\n')
		self.connection.sendall("INSPECT")

		data = self.connection.recv(16)
		self.my_print('received "%s"\n' % data)

		if data == "INSPECT":
			self.my_print("received INSPECT from ABBRobot\n")
			return True 
		else:
			self.my_print("Did no recieve INSPECT from ABBRobot\n")
			return False

	""" HOME """
	""" Move the arm back away from the blisk for the placing and removing of the blisk """
	def pullArmBack(self):

		""" Message Format: (MT_ARM_HOME, BLISK_X, STAGE_X) """
		self.my_print('sending HOME to the client\n')
		self.connection.sendall("HOME")

		data = self.connection.recv(16)
		self.my_print('received "%s"\n' % data)

		if data == "HOME":
			self.my_print("received HOME from ABBRobot\n")
			return True 
		else:
			self.my_print("Did no recieve HOME from ABBRobot\n")
			return False

	""" Send the current force sensing measurement to the controller """
	def sendForceMeasurement(self, reading):

		""" Message Format: (MT_FORCE_MEASUREMENT, measurement) """
		#print "abb force sensing: " + str(reading)

		return True

	""" Handle a message received from the IRC5 controller """
	def handleMessage(self):

		pass

	def closeComm(self):

		self.my_print('closing connection with client\n')
		self.connection.sendall("DISCONNECT")

	def my_print(self, text):
	    sys.stdout.write(str(text))
	    sys.stdout.flush()

""" Questions: Can it handle delays? """


def my_print(text):
    sys.stdout.write(str(text))
    sys.stdout.flush()

def testWrk():

	my_print("in test function\n")
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to the port
	server_address = ('192.168.125.3', 5515)
	my_print('starting up on %s port %s\n' % server_address)
	sock.bind(server_address)

	message = 0
	startTime = time.time()

	# Listen for incoming connections
	sock.listen(1)

	while True:
	    # Wait for a connection
	    my_print('waiting for a connection\n')
	    connection, client_address = sock.accept()

	    try:
	        my_print('connection from ' + str(client_address))

	        # Receive the data in small chunks and retransmit it
	        while True:
				data = connection.recv(16)
				my_print('received "%s"\n' % data)
				if data:
					if (time.time() - startTime > 30):
						my_print('closing connection with client\n')
						connection.sendall("DISCONNECT")
					elif message == 0:
						my_print('sending HOME to the client\n')
						connection.sendall("HOME")
						message += 1
					elif message == 1:
						my_print('sending FAR to the client\n')
						connection.sendall("FAR")
						message += 1
					elif message == 2:
						my_print('sending NEAR to the client\n')
						connection.sendall("NEAR")
						message += 1
					elif message == 3:
						my_print('sending INSPECT to the client\n')
						connection.sendall("INSPECT")
						message = 0
				else:
					my_print('no more data from'+ str(client_address))
					break
					
	            
	    finally:
	        # Clean up the connection
	        connection.close()

""" Used for testing purposes """
if __name__ == "__main__":

	"""abb = ABBRobot()

	for i in range(100):

		abb.sendPacket()
		time.sleep(0.5)"""

	testWrk()

