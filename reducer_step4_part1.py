#!/usr/bin/env python3
import sys
import datetime

def printData(station_id, day, month, year, aggregation_unit, average_prcp):
	if station_id == None:
		return
	if aggregation_unit == 'day':
		print('{0}\t{1}\t{2}'.format( station_id, day, average_prcp ))
	elif aggregation_unit == 'month':
		print('{0}\t{1}\t{2}'.format( station_id, month, average_prcp ))
	else:
		print('{0}\t{1}\t{2}'.format( station_id, year, average_prcp ))

args = sys.argv

aggregation_unit = args[1]

average_prcp = 0
previous_station_id = None
previous_day, previous_month, previous_year = None, None, None
printed_station_id, current_station_id = None, None
prcp_count = 0
previous_type = None

for line in sys.stdin:
	fields = line.split()
	current_station_id, date, type, value, day, month, year = fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6]
	# current_date = datetime.strptime( date ,'%Y%m%d')
	day, month, year, value = int( day ), int( month ), int( year ), int( value )
	
	if (previous_station_id and previous_station_id != current_station_id) or ( aggregation_unit == 'day' and previous_day != day ) or (aggregation_unit == 'month' and previous_month != month) or ( aggregation_unit == 'year' and previous_year != year ):
		if prcp_count == 0:
			prcp_count = 1
		average_prcp = average_prcp / prcp_count
		printData(previous_station_id, previous_day, previous_month, previous_year, aggregation_unit, average_prcp)
		average_prcp = 0
		prcp_count = 0
		printed_station_id = previous_station_id
	
	average_prcp += value
	prcp_count += 1
	previous_station_id = current_station_id
	previous_day, previous_month, previous_year = day, month, year

if current_station_id != printed_station_id:
	if prcp_count == 0:
		prcp_count = 1

	average_prcp = average_prcp / prcp_count
	printData(current_station_id, previous_day, previous_month, previous_year, aggregation_unit, average_prcp)
