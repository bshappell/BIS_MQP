# ABBRobot Class
#import Blisk
import socket
import time
import sys
import struct
import threading
import Queue
 
TCP_IP = "192.168.125.4" #"169.254.118.154" 
TCP_PORT = 5515

class ABBRobot(object):

	def __init__(self):

		self.server_address = (TCP_IP, TCP_PORT)

		""" Create Socket Server Thread to handle TCP communication """
		self.server_thread = SocketServerThread()
		self.server_thread.start()

		self.my_print("setting up server")
		self.server_thread.cmd_q.put(ServerCommand(ServerCommand.SETUP, self.server_address))
		self.portFree = self.server_thread.reply_q.get(True)

		""" Expected response from IRC5 """
		self.exp_message = ""


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
			self.my_print("ERROR Received Incorrect Value: " + str(reply.data) + " Expected: " + expMessage + "\n")
			return False


	""" Check that the arm is up and running, and the connection between the Pi and IRC5 is good """
	def checkConnection(self):

		self.my_print('waiting for a connection\n')
		self.server_thread.cmd_q.put(ServerCommand(ServerCommand.CONNECT, self.server_address))
		reply = self.server_thread.reply_q.get(True)

		return self.receive("CONNECTED")

	""" Position the arm for inspection for the current blisk """
	def positionArmFar(self, currBlisk):

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

	""" Retract the arm from the close position where contact with the blisk was made """
	def retractArm(self, currBlisk):

		if currBlisk == 0:
			self.send("RETRACT_NEAR_P01")
			return self.receive("RETRACT_NEAR_P01")
		elif currBlisk == 1:
			self.send("RETRACT_NEAR_P02")
			return self.receive("RETRACT_NEAR_P02")
		elif currBlisk == 2:
			self.send("RETRACT_NEAR_G02")
			return self.receive("RETRACT_NEAR_G02")
		else: 
			self.my_print("ERROR INCORRECT BLISK NUMBER RECEIVED IN POS ARM CLOSE")
			return False

	""" Position the arm for getting force contact with the blisk """
	def prepInspection(self, position):

		""" Message Format: PREP_BLISK_STAGE_CONCAVE/CONVEX_BB """
		message = "PREP_"
		message += position.blisk_string
		message += "_"
		message += str(position.stage_number)
		message += "_"
		message += str(position.blade_side)
		message += "_"
		message += str(position.ball_bearing)

		self.send(message)
		return self.receive(message)

        """ Send the message to the ABB to move forward more """
	def inspectionPositioning(self):

		self.send("EOAT_FORWARD")
		self.receive("EOAT_FORWARD")

	""" Return whether the abb robot is still in the process of inspecting the blade """
	def stillInspecting(self, position):

		distance = -1
		blade_side = -1	

		""" See if a value has been recieved """
		try:
			ret = self.server_thread.reply_q.get_nowait()
			if ret.data == self.exp_message:
				""" When complete reenable blocking and set inspecting state to false """
				print "received expected data in still inspecting!!!!!!!!!!!"
				return (False, ret.data)
			else:
				self.server_thread.cmd_q.put(ServerCommand(ServerCommand.RECEIVE, self.exp_message))
				return (True, ret.data)

		except Queue.Empty as e:
			return (True, None)

		return (True, None)
                

	""" Inspect the current blade """
	def startInspectBlade(self, position):

		""" Message Format: INSP_BLISK_STAGE_CONCAVE/CONVEX_BB """
		message = "INSP_" 
		message += position.blisk_string
		message += "_"
		message += str(position.stage_number)
		message += "_"
		message += str(position.blade_side)
		message += "_"
		message += str(position.ball_bearing)

		""" Set the expected message """
		self.exp_message = message

		""" Send the message and add the command to receive a response but don't wait for it """
		self.send(message)
		self.server_thread.cmd_q.put(ServerCommand(ServerCommand.RECEIVE, message))
		self.my_print("Start Inspection Blade Function Complete")


	""" Home the arm back away from the blisk for the placing and removing of the blisk """
	def pullArmBack(self):

		""" Message Format: (MT_ARM_HOME, BLISK_X, STAGE_X) """
		self.send("HOME")
		return self.receive("HOME")

	""" Function to close the TCP Socket """
	def closeComm(self):

		self.my_print('closing connection with client\n')
		if self.server_thread:
                        if self.server_thread.connection:
                                self.send("DISCONNECT")
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
            try:
            	self.socket.bind((cmd.data[0], cmd.data[1]))
            except Exception, e:
            	self.my_print("Socket in use, close app")
            	self.reply_q.put(self._error_reply(str(e)))
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

