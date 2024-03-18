#!/usr/bin/env python3
import sys
from datetime import datetime

args = sys.argv
argument_location = args[1]
name_of_location = args[2]
start_date = datetime.strptime( args[3], '%Y%m%d' )
end_date = datetime.strptime( args[4], '%Y%m%d' )

country_code = None
if argument_location == 'country':
	if name_of_location == 'United States':
		country_code = 'US'
	elif name_of_location == 'Canada':
		country_code = 'CA'
	else:
		country_code = 'MX'

selected_statecode = None

with open('ghcnd-states.txt', 'r') as f:
	for line in f:
		fields = line.split()
		state_code, state = fields[0], fields[1]
		if argument_location == 'state' and state == name_of_location:
			selected_statecode = state_code

station_ids = set()

with open('ghcnd-stations.txt', 'r') as f:
	for line in f:
		fields = line.split()
		state_code = fields[4].strip()
		if state_code == selected_statecode or (argument_location == 'station' and name_of_location == fields[0]) or (argument_location == 'country' and fields[0].startswith(country_code)):
			station_ids.add( fields[0] )

for line in sys.stdin:
	fields = line.strip().split(',')
	station_id = fields[0]
	date = fields[1]
	type = fields[2]
	current_date = datetime.strptime( date, '%Y%m%d' )
	year, month, day = current_date.year, current_date.month, current_date.day
	value = fields[3]
	if station_id in station_ids and (start_date <= current_date <= end_date) and type in ('TMAX', 'TMIN', 'TAVG'):
		print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}'.format( station_id, date, type, value, day, month, year ))

