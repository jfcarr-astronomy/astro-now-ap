import geocoder


def BuildDictionary(geocodeObject):
	dictionaryData = {}

	dictionaryData['Latitude'] = geocodeObject.lat
	dictionaryData['Longitude'] = geocodeObject.lng

	return dictionaryData

class CGeocode(object):
	def GetCoordinatesForZipCode(self, zipcode):
		g = geocoder.arcgis(zipcode)

		return BuildDictionary(g)

	def GetCoordinatesForCity(self, city):
		g = geocoder.arcgis(city)

		return BuildDictionary(g)
