# Stage Class


class Stage(object):

	def __init__(self, numberBlades, smallBBRadius, largeBBRadius, stepsArray):

		""" The number of blades on the stage """
		self.numberBlades = numberBlades

		""" Different ball bearing sizes used to inspect the blades of the stage """
		self.largeBBRadius = largeBBRadius
		self.smallBBRadius = smallBBRadius

		""" Array of all the steps for each blade """
		self.stepsArray = stepsArray

	def getNumberBlades(self):
        return self.numberBlades

    def getLargeBBRadius(self):
        return self.largeBBRadius

    def getSmallBBRadius(self):
		return self.smallBBRadius

	def getStepsForBlade(self, blade):

		""" TODO change to use the correct amount!!! """
		return self.stepsArray[0]
