# ABBRobot Class
#import Blisk
import socket
import time
import sys
import struct
import threading
import Queue

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

RECORD_FORCE_SENSING = 0

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

		self.server_address = (TCP_IP, TCP_PORT)
		"""self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind(self.server_address)
		self.socket.listen(2)"""

		""" Create Socket Server Thread to handle TCP communication """
		self.server_thread = SocketServerThread()
		self.server_thread.start()

                self.my_print("setting up server")
		self.server_thread.cmd_q.put(ServerCommand(ServerCommand.SETUP, self.server_address))
		reply = self.server_thread.reply_q.get(True)

		""" Stores the state of whether the ABB is using force sensing feedback or not """
		self.forceFeedback = False
		self.forceStartTime = 0
		self.ff_count = 0

		""" Indicates whether a blade inspection is currently happening """
		self.inspecting = False

		self.my_print("finished abb init")

	""" Send a message to the abb controller """
	def send(self, message):

		self.my_print('sending: ' + message + ' to the client\n')
		self.server_thread.cmd_q.put(ServerCommand(ServerCommand.SEND, message))
		reply = self.server_thread.reply_q.get(True)

	def receive(self, expMessage):
                
		self.server_thread.cmd_q.put(ServerCommand(ServerCommand.RECEIVE, expMessage))
		reply = self.server_thread.reply_q.get(True)

		if reply.data == expMessage:
			self.my_print('Received Expected Value: "%s"\n' % reply.data)
			return True
		else:
			self.my_print("ERROR Received Incorrect Value: " + reply.data + " Expected: " + expMessage + "\n")
			return False


	""" Check that the arm is up and running, and the connection between the Pi and IRC5 is good """
	def checkConnection(self):

		self.my_print('waiting for a connection\n')
		self.server_thread.cmd_q.put(ServerCommand(ServerCommand.CONNECT, self.server_address))
		reply = self.server_thread.reply_q.get(True)

		return self.receive("CONNECTED")

	""" Position the arm for inspection for the current blisk """
	def positionArmFar(self, currBlisk):

		""" Message Format: (MT_ARM_FAR, BLISK_X, STAGE_X) """
		if currBlisk == 0:
			self.send("FAR_P01")
			return self.receive("FAR_P01")
		elif currBlisk == 1:
			self.send("FAR_P02")
			return self.receive("FAR_P02")
		elif currBlisk == 2:
			self.send("FAR_G02")
			return self.receive("FAR_G02")
		else: 
			self.my_print("ERROR INCORRECT BLISK NUMBER RECEIVED IN POS ARM FAR")
			return False


	""" Position the arm for inspection for the current blisk """
	def positionArmClose(self, currBlisk):

		""" Message Format: (MT_ARM_CLOSE, BLISK_X, STAGE_X) """
		if currBlisk == 0:
			self.send("NEAR_P01")
			return self.receive("NEAR_P01")
		elif currBlisk == 1:
			self.send("NEAR_P02")
			return self.receive("NEAR_P02")
		elif currBlisk == 2:
			self.send("NEAR_G02")
			return self.receive("NEAR_G02")
		else: 
			self.my_print("ERROR INCORRECT BLISK NUMBER RECEIVED IN POS ARM CLOSE")
			return False

        """ Send the message to the ABB to move forward more """
	def inspectionPositioning(self):

                self.my_print("move forward more")

                self.send("EOAT_FORWARD")
                self.receive("EOAT_FORWARD")



	""" Position the arm for inspection in the center of the blade using force sensing feedback """
	def positionArmForInspection(self, currBlisk, currStage):

                print "positioning arm for inspection"

		""" Check that the force sensing state is not already active """
		if self.forceFeedback:
			print "ERROR FORCE SENSING FEEDBACK MODE ALREADY SELECTED"
			return

		""" Set the force sensing feedback mode active """
		self.ff_count = 0
		self.forceFeedback = True
		self.forceStartTime = time.time()

		""" Wait until the ABB Robot is finished positioning in the center of the blade """
		while self.forceFeedback:
                        time.sleep(0.01)
			pass

		self.my_print("POSITION ARM FOR INSPECTION COMPLETE")


	""" Return whether the abb robot is still in the process of inspecting the blade """
	def stillInspecting(self, currBlisk, currStage):

		""" Determine the expected message """
		if currStage == 0:
			if currBlisk == 0:
				expMessage = "INSPECT_P01_00"
			elif currBlisk == 1:
				expMessage = "INSPECT_P02_00"
			elif currBlisk == 2:
				expMessage = "INSPECT_G02_00"
			else:
				self.my_print("ERROR INCORRECT BLISK NUMBER RECEIVED IN INSPECTING")
		elif currStage == 1:
			if currBlisk == 2:
				expMessage = "INSPECT_G02_01"
			else:
				self.my_print("ERROR INCORRECT BLISK NUMBER RECEIVED IN INSPECT")
		else:
			self.my_print("ERROR INCORRECT STAGE NUMBER RECEIVED IN INSPECT ")

		distance = -1
		blade_side = -1	

		""" See if a value has been recieved """
		try:
			ret, message = self.server_thread.reply_q.get_nowait()
			if ret.data == expMessage:
				""" When complete reenable blocking and set inspecting state to false """
				print "received expected data in still inspecting!!!!!!!!!!!1"
				self.inspecting = False
				return (False, blade_side, distance)
			else:
				print "POSITION VALUE RECEIVED FROM ABB"
				return (True, blade_side, distance)
		except Queue.Empty as e:
			return (True, blade_side, distance)
		return (True, blade_side, distance)
                

	""" Inspect the current blade """
	def startInspectBlade(self, currBlisk, currStage):

		""" set the state to inspecting """
		self.inspecting = True

		""" Message Format: (MT_INSPECT_BLADE, BLISK_X, STAGE_X) """
		if currStage == 0:
			if currBlisk == 0:
				self.send("INSPECT_P01_00")
			elif currBlisk == 1:
				self.send("INSPECT_P02_00")
			elif currBlisk == 2:
				self.send("INSPECT_G02_00")
			else:
				self.my_print("ERROR INCORRECT BLISK NUMBER RECEIVED IN PINSPECT BLADE")
		elif currStage == 1:
			if currBlisk == 2:
				self.send("INSPECT_G02_01")
			else:
				self.my_print("ERROR INCORRECT BLISK NUMBER RECEIVED IN INSPECT BLADE")
		else:
			self.my_print("ERROR INCORRECT STAGE NUMBER RECEIVED IN INSPECT BLADE")

		self.my_print("recieve val")
		self.server_thread.cmd_q.put(ServerCommand(ServerCommand.RECEIVE, "INSPECT_P02_00"))

		self.my_print("Start Inspection Blade Function Complete")



	""" Home the arm back away from the blisk for the placing and removing of the blisk """
	def pullArmBack(self):

		""" Message Format: (MT_ARM_HOME, BLISK_X, STAGE_X) """
		self.send("HOME")
		return self.receive("HOME")

	""" Send the current force sensing measurement to the controller """
	def sendForceMeasurement(self, reading):

		""" Determine if we are in the force feedback mode """
		if self.forceFeedback:
			self.processForceReading(reading)
			#self.send("FORCE_SENSING"
		else:
			pass

	""" Function to process the force reading and determine if contact has been made """
	def processForceReading(self, reading):

                print "processing force reading"

                self.ff_count += 1

		if time.time() - self.forceStartTime > 5:
			self.forceFeedback = False
			self.my_print("SETTING FORCE FEEDBACK TO FALSE")
			self.my_print("FFB Count: ")
			self.my_print(self.ff_count)

	""" Function to close the TCP Socket """
	def closeComm(self):

		self.my_print('closing connection with client\n')
		if self.server_thread:
			#self.send("DISCONNECT")
			self.server_thread.cmd_q.put(ServerCommand(ServerCommand.CLOSE))
			self.server_thread.join()

        """ Function to handle system prints """
	def my_print(self, text):
	    sys.stdout.write(str(text))
	    sys.stdout.flush()
	    

""" *************************************************************** Server Class *************************************************************** """

""" Code based on code written by Eli Bendersky (eliben@gmail.com) """
""" https://github.com/eliben/code-for-blog/blob/master/2011/socket_client_thread_sample/socketclientthread.py """


class ServerCommand(object):
    """ A command to the server thread.
        Each command type has its associated data:

        CONNECT:    (host, port) tuple
        SEND:       Data string
        RECEIVE:    None
        CLOSE:      None
    """
    CONNECT, SEND, RECEIVE, CLOSE, SETUP = range(5)

    def __init__(self, type, data=None):
        self.type = type
        self.data = data


class ServerReply(object):
    """ A reply from the server thread.
        Each reply type has its associated data:

        ERROR:      The error string
        SUCCESS:    Depends on the command - for RECEIVE it's the received
                    data string, for others None.
    """
    ERROR, SUCCESS = range(2)

    def __init__(self, type, data=None):
        self.type = type
        self.data = data


class SocketServerThread(threading.Thread):
    """ Implements the threading.Thread interface (start, join, etc.) and
        can be controlled via the cmd_q Queue attribute. Replies are
        placed in the reply_q Queue attribute.
    """
    def __init__(self, cmd_q=None, reply_q=None):
        super(SocketServerThread, self).__init__()
        self.cmd_q = cmd_q or Queue.Queue()
        self.reply_q = reply_q or Queue.Queue()
        self.alive = threading.Event()
        self.alive.set()
        self.socket = None
        self.client_address = None
        self.connection = None

        self.handlers = {
            ServerCommand.CONNECT: self._handle_CONNECT,
            ServerCommand.CLOSE: self._handle_CLOSE,
            ServerCommand.SEND: self._handle_SEND,
            ServerCommand.RECEIVE: self._handle_RECEIVE,
            ServerCommand.SETUP: self._handle_SETUP,
        }

    def run(self):
        while self.alive.isSet():
            try:
                # Queue.get with timeout to allow checking self.alive
                cmd = self.cmd_q.get(True, 0.1)
                self.handlers[cmd.type](cmd)
            except Queue.Empty as e:
                continue

    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)


    def _handle_SETUP(self, cmd):

            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((cmd.data[0], cmd.data[1]))
            self.my_print("Binding to socket complete")
            self.socket.listen(2)
            self.my_print("Listening on socket complete")
            self.my_print("setup")

            self.reply_q.put(self._success_reply())

    def _handle_CONNECT(self, cmd):
        try:
            self.my_print("start of connect function")


            self.my_print('waiting for a connection\n')
            self.connection, self.client_address = self.socket.accept()
            self.my_print('connection from ' + str(self.client_address))

            self.reply_q.put(self._success_reply())

        except IOError as e:
            self.reply_q.put(self._error_reply(str(e)))

    def _handle_CLOSE(self, cmd):
        if self.connection:
                self.connection.close()
        reply = ServerReply(ServerReply.SUCCESS)
        self.reply_q.put(reply)

    def _handle_SEND(self, cmd):
        try:
                if self.connection:
                        self.connection.sendall(cmd.data)
                        self.reply_q.put(self._success_reply())
        except IOError as e:
            self.reply_q.put(self._error_reply(str(e)))

    def _handle_RECEIVE(self, cmd):
        try:
        	data = self.connection.recv(16)
        	if data:
        		self.reply_q.put(self._success_reply(data))
        		return
        	else:
        		self.reply_q.put(self._error_reply('Socket closed prematurely'))
        except IOError as e:
        	self.reply_q.put(self._error_reply(str(e)))

    def _error_reply(self, errstr):
        return ServerReply(ServerReply.ERROR, errstr)

    def _success_reply(self, data=None):
        return ServerReply(ServerReply.SUCCESS, data)

    def my_print(self, text):
	    sys.stdout.write(str(text))
	    sys.stdout.flush()


""" Used for testing purposes """
if __name__ == "__main__":

	#testWrk()
	abb = ABBRobot()

