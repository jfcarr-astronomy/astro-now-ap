from datetime import datetime, timedelta
import pytz
import timezonefinder
from astropy.coordinates import EarthLocation, get_body, AltAz
import astropy.units as u
from astropy.time import Time

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

	def GetUTCFromLocalWithCoordinates(self, observerLatitude, observerLongitude, localTime):
		'''
		Given the local observer's latitude, longitude, and datetime, return the local observer's UTC datetime.
		'''
		myTimeZone = self.GetTimeZoneObject(observerLatitude, observerLongitude)

		loc = EarthLocation(lat=observerLatitude*u.deg, lon=observerLongitude*u.deg, height=390*u.m)

		naive_local = self.GetDateTimeFromString(localTime)
		localized_local = self.GetLocalizedTime(naive_local, myTimeZone)
		utc_offset = self.GetUTCOffsetHours(localized_local)*u.hour

		observerUTCDateTime = Time(localTime, scale='utc', location=loc) - utc_offset

		return observerUTCDateTime

	def GetUTCOffsetHours(self, localDateTime):
		return localDateTime.utcoffset().total_seconds()/3600

	def FormatDate(self, inputDate):
		'''
		Given a datetime object, return a nicely formatted string.
		'''
		fmt = '%Y-%m-%d %H:%M:%S %Z'	

		return inputDate.strftime(fmt)
