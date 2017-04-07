import HX711
import time
import RPi.GPIO as GPIO
import numpy
import pigpio # http://abyz.co.uk/rpi/pigpio/python.html
import sys
import struct
import threading
import Queue

CH_A_GAIN_64  = 0 # Channel A gain 64
CH_A_GAIN_128 = 1 # Channel A gain 128
CH_B_GAIN_32  = 2 # Channel B gain 32


class FSCommand(object):
    """ A command to the force sensor thread.
        Each command type has its associated data:

        READING:        None
        PAUSE:   	None
        START: 		None
        END:    	None
    """
    START, PAUSE, READING, END = range(4)

    def __init__(self, type, data=None):
        self.type = type
        self.data = data


class FSReply(object):
    """ A reply from the force sensor thread.
        Each reply type has its associated data:

        ERROR:      The error string
        SUCCESS:    Depends on the command - for RECEIVE it's the received
                    data string, for others None.
    """
    ERROR, SUCCESS = range(2)

    def __init__(self, type, data=None):
        self.type = type
        self.data = data


class FSThread(threading.Thread):
    """ Implements the threading.Thread interface (start, join, etc.) and
        can be controlled via the cmd_q Queue attribute. Replies are
        placed in the reply_q Queue attribute.
    """
    def __init__(self, dataPin, clkPin, cmd_q=None, reply_q=None):
        super(FSThread, self).__init__()
        self.cmd_q = cmd_q or Queue.Queue()
        self.reply_q = reply_q or Queue.Queue()
        self.alive = threading.Event()
        self.alive.set()

        self.dataPin = dataPin
        self.clkPin = clkPin

        """ Use a gain of 128 """
      	self.mode = CH_A_GAIN_128

        """ Set up the Rasp GPIO """
      	self.pi = pigpio.pi()
        if not self.pi.connected:
            print("Error gpio already connected")
            exit(0)

        """ Initialize the HX711 ADC chip """
        self.hx711 = HX711.HX711(self.pi, DATA=self.dataPin, CLOCK=self.clkPin, mode=self.mode, callback=None)

        """ Pause the sensor readings until it has been zeroed """
        self.hx711.pause()

        self.handlers = {
            FSCommand.READING: self._handle_READING,
            FSCommand.START: self._handle_START,
            FSCommand.PAUSE: self._handle_PAUSE,
            FSCommand.END: self._handle_END,
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

    def _handle_READING(self, cmd):

        count, mode, reading = self.hx711.get_reading()
        self.reply_q.put(self._success_reply((count,mode,reading)))

    def _handle_END(self, cmd):
        
        if self.hx711:
        	self.hx711.pause()
        	self.hx711.cancel()
        if self.pi:
        	self.pi.stop()

        self.reply_q.put(FSReply(FSReply.SUCCESS))

    """ Pause the readings from the sensor """
    def _handle_PAUSE(self, cmd):

        self.hx711.pause()
        self.reply_q.put(FSReply(FSReply.SUCCESS))

    """ Start running the sensor """
    def _handle_START(self, cmd):

        self.hx711.start()
        self.reply_q.put(FSReply(FSReply.SUCCESS))

    def _error_reply(self, errstr):
        return FSReply(FSReply.ERROR, errstr)

    def _success_reply(self, data=None):
        return FSReply(FSReply.SUCCESS, data)

    def my_print(self, text):
	    sys.stdout.write(str(text))
	    sys.stdout.flush()

