# Blisk Class

class Blisk(object):

	def __init__(self, bliskID, inspectionTime, firstStage, secondStage):

                self.bliskID = bliskID
		self.inspectionTime = inspectionTime
		self.firstStage = firstStage
		self.secondStage = secondStage

	def getBliskID(self):
                return self.bliskID

	def getFirstStage(self):
                return self.firstStage

        def getSecondStage(self):
                return self.secondStage

        def getInspectionTime(self):
                return self.inspectionTime
		
