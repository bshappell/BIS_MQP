# Stage Class


class Stage(object):

	def __init__(self, numberBlades, largeBBRadius, smallBBRadius):

		self.numberBlades = numberBlades
		self.largeBBRadius = largeBBRadius
		self.smallBBRadius = smallBBRadius

	def getNumberBlades(self):
                return self.numberBlades

        def getLargeBBRadius(self):
                return self.largeBBRadius

        def getSmallBBRadius(self):
		return self.smallBBRadius
