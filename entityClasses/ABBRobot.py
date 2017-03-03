# ABBRobot Class
#import Blisk
import socket
import time
import sys

TCP_IP = "192.168.125.2" 
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

	""" Send a message to the abb controller """
	def send(self, message):

		self.my_print('sending: ' + message + ' to the client\n')
		self.connection.sendall(message)

	def receive(self, expMessage):

		data = self.connection.recv(16)

		if data == expMessage:
			self.my_print('Received Expected Value: "%s"\n' % data)
			return True 
		else:
			self.my_print("ERROR Received Incorrect Value: " + data + " Expected: " + expMessage + "\n")
			return False

	""" Check that the arm is up and running, and the connection between the Pi and IRC5 is good """
	def checkConnection(self):

		self.my_print('waiting for a connection\n')
		self.connection, self.client_address = self.socket.accept()
		self.my_print('connection from ' + str(self.client_address))

		return self.receive("CONNECTED")

	""" Position the arm for inspection for the current blisk """
	def positionArmFar(self, currBlisk):

		""" Message Format: (MT_ARM_FAR, BLISK_X, STAGE_X) """
		if currBlisk == 0:
			self.send("FAR_00")
			return self.receive("FAR_00")
		elif currBlisk == 1:
			self.send("FAR_01")
			return self.receive("FAR_01")
		elif currBlisk == 2:
			self.send("FAR_02")
			return self.receive("FAR_02")
		else: 
			self.my_print("ERROR INCORRECT BLISK NUMBER RECEIVED IN POS ARM FAR")
			return False


	""" Position the arm for inspection for the current blisk """
	def positionArmClose(self, currBlisk):

		""" Message Format: (MT_ARM_CLOSE, BLISK_X, STAGE_X) """
		if currBlisk == 0:
			self.send("NEAR_00")
			return self.receive("NEAR_00")
		elif currBlisk == 1:
			self.send("NEAR_01")
			return self.receive("NEAR_01")
		elif currBlisk == 2:
			self.send("NEAR_02")
			return self.receive("NEAR_02")
		else: 
			self.my_print("ERROR INCORRECT BLISK NUMBER RECEIVED IN POS ARM CLOSE")
			return False


	""" Inspect the current blade """
	def inspectBlade(self, currBlisk, currStage):

		""" Message Format: (MT_INSPECT_BLADE, BLISK_X, STAGE_X) """
		if currStage == 0:
			if currBlisk == 0:
				self.send("INSPECT_00_00")
				return self.receive("INSPECT_00_00")
			elif currBlisk == 1:
				self.send("INSPECT_01_00")
				return self.receive("INSPECT_01_00")
			elif currBlisk == 2:
				self.send("INSPECT_02_00")
				return self.receive("INSPECT_02_00")
			else:
				self.my_print("ERROR INCORRECT BLISK NUMBER RECEIVED IN PINSPECT BLADE")
				return False
		elif currStage == 1:
			if currBlisk == 0:
				self.send("INSPECT_00_01")
				return self.receive("INSPECT_00_01")
			elif currBlisk == 1:
				self.send("INSPECT_01_01")
				return self.receive("INSPECT_01_01")
			elif currBlisk == 2:
				self.send("INSPECT_02_01")
				return self.receive("INSPECT_02_01")
			else:
				self.my_print("ERROR INCORRECT BLISK NUMBER RECEIVED IN INSPECT BLADE")
				return False
		else:
			self.my_print("ERROR INCORRECT STAGE NUMBER RECEIVED IN INSPECT BLADE")
			return False


	""" Home the arm back away from the blisk for the placing and removing of the blisk """
	def pullArmBack(self):

		""" Message Format: (MT_ARM_HOME, BLISK_X, STAGE_X) """
		self.send("HOME")
		return self.receive("HOME")

	""" Send the current force sensing measurement to the controller """
	def sendForceMeasurement(self, reading):

		""" Message Format: (MT_FORCE_MEASUREMENT, measurement) """
		#print "abb force sensing: " + str(reading)
		return True


	def closeComm(self):

		self.my_print('closing connection with client\n')
		self.connection.sendall("DISCONNECT")

	def my_print(self, text):
	    sys.stdout.write(str(text))
	    sys.stdout.flush()

""" *************************************************************** TEST CODE *************************************************************** """

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
				time.sleep(5)
				if data:
					if (time.time() - startTime > 30):
						my_print('closing connection with client\n')
						connection.sendall("DISCONNECT")
					elif message == 0:
						my_print('sending HOME to the client\n')
						#time.sleep(1)
						connection.sendall("HOME")
						message += 1
					elif message == 1:
						#time.sleep(1)
						my_print('sending FAR to the client\n')
						connection.sendall("FAR")
						message += 1
					elif message == 2:
						#time.sleep(1)
						my_print('sending NEAR to the client\n')
						connection.sendall("NEAR")
						message += 1
					elif message == 3:
						#time.sleep(1)
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

	testWrk()

