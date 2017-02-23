# ABBRobot Class
#import Blisk
import socket
import time

UDP_IP = "192.168.125.1" # IRC5 Controller
# Lab PC is 192.168.125.2
# This pc is 192.168.125.3
UDP_PORT = 5515
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
MT_INSPECTION_COMPLETE = 0x09

class ABBRobot(object):

	def __init__(self):

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

	""" Used to test sending packets """
	def sendPacket(self):

		self.socket.sendto(MESSAGE, (UDP_IP, UDP_PORT))


	""" Check that the arm is up and running, and the connection between the Pi and IRC5 is good """
	def checkConnection(self):

		""" Return whether the connection was successful of not """
		return True 

	""" Position the arm for inspection for the current blisk """
	def positionArmFar(self, currBlisk):

		""" Message Format: (MT_ARM_FAR, BLISK_X, STAGE_X) """

		return True

	""" Position the arm for inspection for the current blisk """
	def positionArmClose(self, currBlisk):

		""" Message Format: (MT_ARM_CLOSE, BLISK_X, STAGE_X) """

		return True

	""" Position arm for inspection of the blade """
	def posArmForInspection(self, currBlisk, currStage):

		return True

	""" Inspect the current blade """
	def inspectBlade(self, currBlisk, currStage):

		""" Message Format: (MT_INSPECT_BLADE, BLISK_X, STAGE_X) """

		return True

	""" Move the arm back away from the blisk for the placing and removing of the blisk """
	def pullArmBack(self):

		""" Message Format: (MT_ARM_HOME, BLISK_X, STAGE_X) """

		return True

	""" Send the current force sensing measurement to the controller """
	def sendForceMeasurement(self, measurement):

		""" Message Format: (MT_FORCE_MEASUREMENT, measurement) """

		return True

	""" Handle a message received from the IRC5 controller """
	def handleMessage(self):

		pass

def UdpRecvTest():

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #DGRAM) # UDP
	sock.bind(('192.168.125.1', UDP_PORT))
	#time_init = time.time()
	"""while time.time() < 100 + time_init:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		print "received message:", data
		print "recieved from : ", addr
		print "meh"
		"""

	sock.listen(1)
	conn, addr = sock.accept()
	print 'Connection address:', addr
	while 1:
		data = conn.recv(BUFFER_SIZE)
		if not data: break
		print "received data:", data
		#conn.send(data)  # echo

	conn.close()

import sys


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
	                my_print('sending data back to the client')
	                connection.sendall(data)
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

	#UdpRecvTest()
	testWrk()

