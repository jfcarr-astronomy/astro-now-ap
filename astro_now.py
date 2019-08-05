from datetime import datetime, timedelta
import pytz
import timezonefinder

class CAstroNow(object):
	def __init__(self, observerLatitude, observerLongitude, observerUTCDateTime):
		self.observerLatitude = observerLatitude
		self.observerLongitude = observerLongitude
		self.observerUTCDateTime = observerUTCDateTime

	def DumpDebug(self):
		print("Observer Latitude and Longitude is {latitude} and {longitude}".format(latitude=self.observerLatitude,longitude=self.observerLongitude))
		print("Observer UTC date and time is {observerUTCDateTime}".format(observerUTCDateTime=self.observerUTCDateTime))

class CTimeZoneManager(object):
	'''
	Time zone operations.
	'''
	def __init__(self):
		'''
		Currently no constructor needed.
		'''
		pass

	def GetDateTimeFromString(self, strDateTime):
		'''
		Converts string to a datetime object.

		Required string format:  YYYY-MM-DD hh:mm
		'''
		return datetime.strptime(strDateTime, "%Y-%m-%d %H:%M")

	def GetTimeZoneObject(self, latitude, longitude):
		'''
		Given latitude and longitude geographic coordinates, return a pytz timezone object.
		'''
		tf = timezonefinder.TimezoneFinder()

		timeZoneStr = tf.certain_timezone_at(lat=latitude, lng=longitude)

		return pytz.timezone(tf.certain_timezone_at(lat=latitude, lng=longitude))

	def GetLocalFromUTC(self, utcDateTime, localTimeZone):
		'''
		Given a utc datetime, and a local time zone object, return the utc time converted to local time.
		'''
		utc_timezone = pytz.timezone("utc")
		utcDateTime = utc_timezone.localize(utcDateTime, is_dst=None)

		loc_dt = utcDateTime.astimezone(localTimeZone)

		return loc_dt

	def GetLocalizedTime(self, localDateTime, localTimeZone):
		'''
		Given a naive local datetime and a timezone object, return a localized datetime.
		'''
		local_timezone = pytz.timezone (localTimeZone.zone)

		return local_timezone.localize(localDateTime, is_dst=None)

	def GetUTCFromLocal(self, localDateTime, localTimeZone):
		'''
		Given a local datetime, and a local timezone object, return the local time converted to utc time.

		(The input datetime is naive, meaning you don't have to know if Daylight Savings is in effect.)
		'''
		local_timezone = pytz.timezone (localTimeZone.zone)
		input_local = local_timezone.localize(localDateTime, is_dst=None)
		output_utc = input_local.astimezone(pytz.utc)

		return output_utc		

	def GetUTCOffsetHours(self, localDateTime):
		return localDateTime.utcoffset().total_seconds()/3600

	def FormatDate(self, inputDate):
		'''
		Given a datetime object, return a nicely formatted string.
		'''
		fmt = '%Y-%m-%d %H:%M:%S %Z'	

		return inputDate.strftime(fmt)
