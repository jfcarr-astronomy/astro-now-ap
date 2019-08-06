class CAstroNow(object):
	def __init__(self, observerLatitude, observerLongitude, observerUTCDateTime):
		self.observerLatitude = observerLatitude
		self.observerLongitude = observerLongitude
		self.observerUTCDateTime = observerUTCDateTime

	def DumpDebug(self):
		print("Observer Latitude and Longitude is {latitude} and {longitude}".format(latitude=self.observerLatitude,longitude=self.observerLongitude))
		print("Observer UTC date and time is {observerUTCDateTime}".format(observerUTCDateTime=self.observerUTCDateTime))
