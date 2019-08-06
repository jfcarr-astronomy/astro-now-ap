#!/usr/bin/python3

import argparse
from datetime import datetime, timedelta
import sys

# Local libraries
import lib.astro_now as AstroNow
import lib.geocode as GeoCode
import lib.timezone as TimeZone

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
		myGeocoder = GeoCode.CGeocode()
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

	myTZM = TimeZone.CTimeZoneManager()

	observerUTCDateTime = myTZM.GetUTCFromLocalWithCoordinates(myCoordinates["Latitude"], myCoordinates["Longitude"], observerDateTime)

	myAstro = AstroNow.CAstroNow(observerLatitude=myCoordinates["Latitude"], observerLongitude=myCoordinates["Longitude"], observerUTCDateTime=observerUTCDateTime)

	myAstro.DumpDebug()

if __name__ == '__main__':
	sys.exit(main(sys.argv))