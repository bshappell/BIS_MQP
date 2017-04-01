

import csv
import datetime
import InspectionPosition

""" Class to handle saving the inspection results """
class InspectionResults(object):

	def __init__(self):

		self.filename = None
		self.file = None
		self.bliskID = None
		self.csvWriter = None

	""" Make a new file to store the inspection results for the blisk """
	def openNewFile(self, bliskID):

		""" See if a file was already open, if so close it """
		if(self.filename):
			self.closeFile()
			self.file = None
			self.filename = None

		""" Open the file and create a csv writer """
		self.filename = datetime.datetime.now().strftime("/home/pi/Documents/BIS_MQP/results/Blisk" + bliskID + "_%B_%d_%Y_%I%M%p" + ".csv")
		self.file = open(self.filename, 'wb')
		print self.filename
		self.csvWriter = csv.writer(self.file)
		self.bliskID = bliskID	

		""" Write the Header Row """
		self.csvWriter.writerow(("Stage", "Blade", "Blade Side", "small Ball Bearing", "Position", "Result"))

	""" Add a new line to the csv file """
	def addResult(self, position, result):

                self.csvWriter.writerow((position.stage_number, position.blade_number, position.blade_side, position.small_ball_bearing, position.distance, result))


	""" Close the current file """
	def closeFile(self):

		self.file.close()
		self.filename = None
		self.file = None
		
