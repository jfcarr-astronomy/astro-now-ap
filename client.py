#!/usr/bin/python3

import argparse
from datetime import datetime, timedelta
import sys
from astropy.coordinates import EarthLocation, get_body, AltAz
import astropy.units as u
from astropy.time import Time

# Local libraries
import astro_now as anow
import geocode as GC

def main(args):
	parser = argparse.ArgumentParser()

	try:
		parser.add_argument("-coordinates", type=str, help="Location, in the form 'Latitude,Longitude', e.g., '39.764200,-84.188201'")
		parser.add_argument("-date", type=str, help="Date and time, in the form 'yyyy-mm-dd hh:mm:ss', e.g., '2017-06-11 22:15:00'.  If omitted, current date/time is used.")
		parser.add_argument("-location", type=str, help="Location, in the form 'City, State', e.g., 'Dayton, OH'")
		args = parser.parse_args()
	except Exception as ex:
		sys.stderr.write(ex)
		sys.exit(1)

	if args.location:
		myGeocoder = GC.CGeocode()
		myCoordinates = myGeocoder.GetCoordinatesForCity(args.location)
		if myCoordinates['Latitude'] == None:
			print("Geocoder is unavailable.")
			sys.exit(-1)
	else:
		if args.coordinates:
			coordinate_args = args.coordinates.split(',')
			myCoordinates = {'Latitude': coordinate_args[0], 'Longitude': coordinate_args[1]}
		else:
			print("Location or Coordinates are required.")
			sys.exit(-1)

	if args.date:
		observerDateTime = args.date
	else:
		observerDateTime = datetime.now().strftime('%Y-%m-%d %H:%M')

	myTZM = anow.CTimeZoneManager()

	myTimeZone = myTZM.GetTimeZoneObject(myCoordinates["Latitude"], myCoordinates["Longitude"])

	loc = EarthLocation(lat=myCoordinates["Latitude"]*u.deg, lon=myCoordinates["Longitude"]*u.deg, height=390*u.m)

	naive_local = myTZM.GetDateTimeFromString(observerDateTime)
	localized_local = myTZM.GetLocalizedTime(naive_local, myTimeZone)
	utc_offset = myTZM.GetUTCOffsetHours(localized_local)*u.hour

	observerUTCDateTime = Time(observerDateTime, scale='utc', location=loc) - utc_offset

	myAstro = anow.CAstroNow(observerLatitude=myCoordinates["Latitude"], observerLongitude=myCoordinates["Longitude"], observerUTCDateTime=observerUTCDateTime)

	myAstro.DumpDebug()

if __name__ == '__main__':
	sys.exit(main(sys.argv))