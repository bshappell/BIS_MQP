# ForceSensor Class

""" Occasionally was working, stopped working after adding pwm to tool switch but that is most likely not the cause"""

READING_TO_GRAMS = -0.00236
PLOTTING = 0
F_THRESH = 1750

import FSThread
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

        """ Used to store the initial y intercept """
        self.y_init = 0 
                    
        """ Create Force Sensor Thread """
        self.fs_thread = FSThread.FSThread(self.dataPin, self.clkPin)
        self.fs_thread.start()

    """ Pause the readings from the sensor """
    def pauseReadings(self):

        self.fs_thread.cmd_q.put(FSThread.FSCommand(FSThread.FSCommand.PAUSE))
        reply = self.fs_thread.reply_q.get(True)

    """ Start running the sensor """
    def startReadings(self):

        self.fs_thread.cmd_q.put(FSThread.FSCommand(FSThread.FSCommand.START))
        reply = self.fs_thread.reply_q.get(True)
        time.sleep(0.5)

    """ Get a reading from the force sensor """
    def get_reading(self):

        self.fs_thread.cmd_q.put(FSThread.FSCommand(FSThread.FSCommand.READING))
        reply = self.fs_thread.reply_q.get(True)
        return reply.data

    """ Processes the force sensing readings until the arm is correctly positioned in the fillet """
    def positionInFillet(self, callFunc):

        saveCount = 0

        """ Start receving readings """
        self.startReadings()

        readings = []
        timeList = []

        start_time = time.time()
        #print start_time

        c,m,r = self.get_reading()
        #c-=1
        time.sleep(0.1)
        last_val = 0
        restartCount = 0
        mvCmd_cnt = 0
        
        """ Collect multiple readings to be averaged """
        while(time.time()-start_time < 20):

            count, mode, reading = self.get_reading()
            #c+=1
            #print "Reading = "
            #print(reading)
            #print count, mode, reading

            #print "count: " + str(count)
            #print "c: " + str(c)

            if(count != c):
                last_val = time.time()
                c = count

            if (count == c) and (time.time() - last_val >= 0.02):
                restartCount += 1
                print "restarting HX711"
                self.restartHX711()
                c,m,r = self.get_reading()
                last_val = time.time()
            else:
                #print "Getting Reading"
                gramsReading = READING_TO_GRAMS  * (reading - self.y_init)
                print gramsReading
                readings.append(gramsReading)
                timeList.append(time.time()-start_time)
                time.sleep(0.03)
                if(gramsReading < F_THRESH):
                    """ Send the value to the abb """
                    mvCmd_cnt +=1
                    #print "Sending Move Command"
                    callFunc()

                elif(gramsReading >= F_THRESH):
                    print "Force Sensing Threshold Detected, Exiting Force Sensing Loop"
                    break

        """ Pause readings when function complete """
        self.pauseReadings()

        print restartCount
        print "Move Commands Sent: ", mvCmd_cnt

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
        count, mode, reading = self.get_reading()
        while(reading == None) and (time.time() - startTime < 10):

            """ Start gettings readings """
            self.restartHX711()
            count, mode, reading = self.get_reading()

        """ Collect multiple readings to be averaged """
        for i in range(10):

            count, mode, reading = self.get_reading()
            #print "Reading = "
            #print(reading)
            #print count, mode, reading
            averages.append(reading)
            time.sleep(0.04)

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
        self.pauseReadings()
        time.sleep(0.1)
        self.startReadings()  

    def end(self):
                  
        self.fs_thread.cmd_q.put(FSThread.FSCommand(FSThread.FSCommand.END))
        reply = self.fs_thread.reply_q.get(True)
        self.fs_thread.join()



def testFunc():

    #print "value received"
    pass

""" For testing purposes """
if __name__=="__main__":

    fs = ForceSensor(24,23)

    fs.zeroSensor()
    time.sleep(1) # number of seconds of testing, increase as needed
    print "Start"
    fs.positionInFillet(testFunc)
    #fs.zeroSensor()
    #fs.startReadings()
    #fs.startReadings()
    fs.end()

