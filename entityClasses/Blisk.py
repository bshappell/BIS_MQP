# Blisk Class

class Blisk(object):

        def __init__(self, bliskID, inspectionTime, stages):

                self.bliskID = bliskID
                self.inspectionTime = inspectionTime
                self.stages = stages

        def getBliskID(self):
                return self.bliskID

	def getFirstStage(self):
                return self.stages[0]

        def getSecondStage(self):
                if(len(self.stages)>1):
                        return self.stages[1]
                else:
                        return None

        def getInspectionTime(self):
                return self.inspectionTime
		
