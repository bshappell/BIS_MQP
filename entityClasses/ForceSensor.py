# ForceSensor Class

""" Occasionally was working, stopped working after adding pwm to tool switch but that is most likely not the cause"""

CH_A_GAIN_64  = 0 # Channel A gain 64
CH_A_GAIN_128 = 1 # Channel A gain 128
CH_B_GAIN_32  = 2 # Channel B gain 32
READING_TO_GRAMS = -0.00236
PLOTTING = 0
F_THRESH = 1750

import csv
import time
import RPi.GPIO as GPIO
import numpy
import pigpio # http://abyz.co.uk/rpi/pigpio/python.html
import matplotlib.pyplot as plt

class ForceSensor(object):

    def __init__(self, dataPin, clkPin, forceCallback=None):

        """ Set up the data and clock pins """
      	self.clkPin = clkPin
      	self.dataPin = dataPin

      	""" Function to send force reading to """
      	if forceCallback:
            self.forceCallback = forceCallback
        else:
            None #self.forceCallback = forceReadingCallback

      	""" Use a gain of 128 """
      	self.mode = CH_A_GAIN_128

      	""" Used to store the initial y intercept """
      	self.y_init = 0 
                    
        """ Set up the Rasp GPIO """
      	self.pi = pigpio.pi()
        if not self.pi.connected:
            print("Error gpio already connected")
            exit(0)

        """ Initialize the HX117 ADC chip """
        self.hx117 = HX711(self.pi, DATA=self.dataPin, CLOCK=self.clkPin, mode=self.mode, callback=self.forceReadingCallback)

        """ Pause the sensor readings until it has been zeroed """
        self.hx117.pause()

    """ Callback for when a new reading is recieved from the force sensor """
    def forceReadingCallback(self, count, mode, reading):

        gramsReading = READING_TO_GRAMS  * (reading - self.y_init)
        
        """ Send the values to the IRC5 Controller """
        self.forceCallback(count, mode, gramsReading)

    """ Pause the readings from the sensor """
    def pauseReadings(self):

        self.hx117.pause()

    """ Start running the sensor """
    def startReadings(self):

        self.hx117.start()
        time.sleep(1)

    """ Processes the force sensing readings until the arm is correctly positioned in the fillet """
    def positionInFillet(self, callFunc):

        saveCount = 0

        """ Start receving readings """
        self.startReadings()

        readings = []
        timeList = []

        start_time = time.time()
        #print start_time

        c,m,r = self.hx117.get_reading()
        c-=1
        time.sleep(0.1)
        
        """ Collect multiple readings to be averaged """
        while(True):  # time.time()-start_time < 20):

            count, mode, reading = self.hx117.get_reading()
            c+=1
            #print "Reading = "
            #print(reading)
            #print count, mode, reading

            if (count == c):
                print "restarting HX711"
                self.restartHX711()
            else:
                print "Getting Reading"
                gramsReading = READING_TO_GRAMS  * (reading - self.y_init)
                print gramsReading
                readings.append(gramsReading)
                timeList.append(time.time()-start_time)
                time.sleep(0.07)
                saveCount = count - c
                if(gramsReading < F_THRESH):
                    """ Send the value to the abb """
                    print "Sending Move Command"
                    callFunc()

                elif(gramsReading >= F_THRESH):
                    print "Exiting Force Sensing Loop"
                    break

        """ Pause readings when function complete """
        self.pauseReadings()

        print "Number of Samples:" + str(saveCount)

        if(PLOTTING):
            with open('data.csv', 'wb') as f:
                writer = csv.writer(f)
                for value in range(0, len(readings)):
                    writer.writerow([readings[value], timeList[value]])
            plt.plot(timeList,readings)
            plt.ylabel('Force (g)')
            plt.show()

        print "position in fillet complete"


    """ Zero the sensor by polling it over a time frame """
    def zeroSensor(self):

        print "Starting Zeroing Function """
        startTime = time.time()

        """ Start gettings readings """
        self.startReadings()

        """ List to store the average reading values """
        averages = []

        """ Check that the reading isnt currently None """
        count, mode, reading = self.hx117.get_reading()
        while(reading == None) and (time.time() - startTime < 10):

            """ Start gettings readings """
            self.pauseReadings()
            time.sleep(1)
            self.startReadings()
            time.sleep(1)
            count, mode, reading = self.hx117.get_reading()

        """ Collect multiple readings to be averaged """
        for i in range(50):

            count, mode, reading = self.hx117.get_reading()
            #print "Reading = "
            #print(reading)
            #print count, mode, reading
            averages.append(reading)
            time.sleep(0.1)

        """ Remove the outliers """
        """ TODO Remove Outliers """

        """ Take the average of the array """
        print "averages: "
        print averages
        if averages[0]:
            self.y_init = numpy.mean(numpy.array(averages))
        else:
            print "ERROR No Force Sensor Readings"

        """ Pause the readings """
        self.pauseReadings()

        print "Zeroing Function Complete"


    def restartHX711(self):
        self.hx117.pause()
        time.sleep(0.1)
        self.startReadings()
        

    def end(self):
                  
        self.hx117.pause()
        self.hx117.cancel()
        self.pi.stop()
              

""" Code taken from http://abyz.co.uk/rpi/pigpio/examples.html#Python_HX711_py """
class HX711:

 """
 A class to read the HX711 24-bit ADC.
 """

 def __init__(self, pi, DATA, CLOCK, mode=CH_A_GAIN_128, callback=None):
    """
    Instantiate with the Pi, the data GPIO, and the clock GPIO.

    Optionally the channel and gain may be specified with the
    mode parameter as follows.

    CH_A_GAIN_64  - Channel A gain 64
    CH_A_GAIN_128 - Channel A gain 128
    CH_B_GAIN_32  - Channel B gain 32

    Optionally a callback to be called for each new reading may be
    specified.  The callback receives three parameters, the count,
    the mode, and the reading.  The count is incremented for each
    new reading.
    """
    self.pi = pi
    self.DATA = DATA
    self.CLOCK = CLOCK
    self.set_mode(mode)
    self.callback = callback

    self._paused = False
    self._data_level = 0
    self._clocks = -1
    self._value = 0
    self._reading = None
    self._count = 0

    pi.set_mode(CLOCK, pigpio.OUTPUT)
    pi.set_mode(DATA, pigpio.INPUT)

    pi.write(CLOCK, 1) # Pause the sensor.

    pi.wave_add_generic(
       [pigpio.pulse(1<<CLOCK, 0, 20), pigpio.pulse(0, 1<<CLOCK, 20)]) #was 20 and 20 not 2 and 2

    self._wid = pi.wave_create()

    self._cb1 = pi.callback(DATA, pigpio.EITHER_EDGE, self._callback)
    self._cb2 = pi.callback(CLOCK, pigpio.FALLING_EDGE, self._callback)

    self._valid_after = time.time() + 0.4

    pi.write(CLOCK, 0) # Start the sensor.

 def get_reading(self):
    """
    Returns the current count, mode, and reading.

    The count is incremented for each new reading.
    """
    return self._count, self._mode, self._reading

 def set_callback(self, callback):
    """
    Sets the callback to be called for every new reading.
    The callback receives three parameters, the count,
    the mode, and the reading.  The count is incremented
    for each new reading.

    The callback can be cancelled by passing None.
    """
    self.callback = callback

 def set_mode(self, mode):
    """
    Sets the mode.

    CH_A_GAIN_64  - Channel A gain 64
    CH_A_GAIN_128 - Channel A gain 128
    CH_B_GAIN_32  - Channel B gain 32
    """
    self._mode = mode

    if mode == CH_A_GAIN_128:
       self._pulses = 25
    elif mode == CH_B_GAIN_32:
       self._pulses = 26
    elif mode == CH_A_GAIN_64:
       self._pulses = 27
    else:
       raise ValueError

    self._valid_after = time.time() + 0.4

 def get_mode(self):
    """
    Returns the current mode.
    """
    return self._mode

 def pause(self):
    """
    Pauses readings.
    """
    self._paused = True
    self.pi.wave_tx_stop()
    self.pi.write(self.CLOCK, 1)
    self.pi.set_watchdog(self.CLOCK, 0) # Cancel any timeout.

 def start(self):
    """
    Starts readings.
    """
    self.pi.write(self.CLOCK, 0)
    self._clocks = -1
    self._value = 0
    self._paused = False
    self._valid_after = time.time() + 0.4

 def cancel(self):
    """
    Cancels the sensor and release resources.
    """
    if self._cb1 is not None:
       self._cb1.cancel()
       self._cb1 = None

    if self._cb2 is not None:
       self._cb2.cancel()
       self._cb2 = None

    if self._wid is not None:
       self.pi.wave_delete(self._wid)
       self._wid = None

    self.pi.set_watchdog(self.CLOCK, 0) # cancel timeout

 def _callback(self, gpio, level, tick):

    if gpio == self.CLOCK:

       if level == 0:

          self._clocks += 1

          if self._clocks < 25:

             self._value = (self._value << 1) + self._data_level

       else: #  timeout

          self.pi.set_watchdog(self.CLOCK, 0) # cancel timeout

          if self._clocks == self._pulses:
             if self._value & 0x800000:
                self._value |= ~0xffffff

             if not (self._paused) and (time.time() > self._valid_after):
                self._reading = self._value
                self._count += 1
                if self.callback is not None:
                   self.callback(self._count, self._mode, self._reading)

          self._clocks = 0
          self._value = 0

    else:

       self._data_level = level

       if (level == 0) and (self._clocks == 0):

          if not self._paused:
             self.pi.wave_chain([255, 0, self._wid, 255, 1, self._pulses, 0])
             self.pi.set_watchdog(self.CLOCK, 2) # 2 ms timeout



def forceReadingCallback(count, mode, reading):

        #print "raw reading: " + str(reading)

        gramsReading = READING_TO_GRAMS  * (reading)
        #print(count, mode, round(gramsReading, 2))


def testFunc():

    print "value received"


""" For testing purposes """
if __name__=="__main__":

    fs = ForceSensor(24,23, forceReadingCallback)

    fs.zeroSensor()
    time.sleep(1) # number of seconds of testing, increase as needed
    print "Start"
    fs.positionInFillet(testFunc)
    #fs.zeroSensor()
    #fs.startReadings()
    #fs.startReadings()
    #time.sleep(10)
    fs.end()

