#!/usr/bin/env python3
import sys
from datetime import datetime

args = sys.argv
argument_location = args[1]
name_of_location1 = args[2]
name_of_location2 = args[3]
start_date = datetime.strptime( args[4], '%Y%m%d' )
end_date = datetime.strptime( args[5], '%Y%m%d' )

country_code = None
if argument_location == 'country':
	if name_of_location1 == 'United States' or name_of_location2 == 'United States':
		country_code = 'US'
	elif name_of_location1 == 'Canada' or name_of_location2 == 'Canada':
		country_code = 'CA'
	else:
		country_code = 'MX'

selected_statecode = set()
statecode_state_map = dict()
station_state_map = dict()

with open('ghcnd-states.txt', 'r') as f:
	for line in f:
		fields = line.split()
		state_code, state = fields[0], fields[1]
		if argument_location == 'state' and (state == name_of_location1 or state == name_of_location2):
			selected_statecode.add( state_code )
			statecode_state_map[state_code] = state

station_ids = set()

with open('ghcnd-stations.txt', 'r') as f:
	for line in f:
		fields = line.split()
		state_code = fields[4].strip()
		if state_code in selected_statecode or (argument_location == 'station' and (name_of_location1 == fields[0] or name_of_location2 == fields[0])) or (argument_location == 'country' and fields[0].startswith(country_code)):
			station_ids.add( fields[0] )
			station_state_map[ fields[0] ] = statecode_state_map[state_code]

for line in sys.stdin:
	fields = line.strip().split(',')
	station_id = fields[0]
	date = fields[1]
	type = fields[2]
	current_date = datetime.strptime( date, '%Y%m%d' )
	year, month, day = current_date.year, current_date.month, current_date.day
	value = fields[3]
	if station_id in station_ids and (start_date <= current_date <= end_date) and type in ('TMAX', 'TMIN', 'TAVG'):
		if argument_location == 'country':
			print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}'.format( station_id, date, type, value, day, month, year, argument_location, country_code ))
		elif argument_location == 'station':
			print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}'.format( station_id, date, type, value, day, month, year, argument_location, station_id ))
		else:
			print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}'.format( station_id, date, type, value, day, month, year, argument_location, station_state_map[station_id] ))
