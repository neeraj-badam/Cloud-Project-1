#!/usr/bin/env python3
import sys
import datetime

def printData(station_id, day, month, year, aggregation_unit, average_tmax, avarage_tmin, average_tavg):
	if aggregation_unit == 'day':
		print('{0}\t{1}\t{2}\t{3}\t{4}'.format( station_id, day, average_tmax, average_tmin, average_tavg ))
	elif aggregation_unit == 'month':
		print('{0}\t{1}\t{2}\t{3}\t{4}'.format( station_id, month, average_tmax, average_tmin, average_tavg ))
	else:
		print('{0}\t{1}\t{2}\t{3}\t{4}'.format( station_id, year, average_tmax, average_tmin, average_tavg ))

args = sys.argv

aggregation_unit = args[1]

# average_temperature = 0
current_station_id = None
average_tmax, average_tmin, average_tavg = 0, 0, 0
previous_station_id = None
previous_day, previous_month, previous_year = None, None, None
printed_station_id = None
tmax_count, tmin_count, tavg_count = 0, 0, 0
previous_type = None

for line in sys.stdin:
	fields = line.split()
	current_station_id, date, type, value, day, month, year = fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6]
	# current_date = datetime.strptime( date ,'%Y%m%d')
	day, month, year, value = int( day ), int( month ), int( year ), int( value )
	
	if (previous_station_id and previous_station_id != current_station_id) or ( aggregation_unit == 'day' and previous_day != day ) or (aggregation_unit == 'month' and previous_month != month) or ( aggregation_unit == 'year' and previous_year != year ):
		if tmax_count == 0 :
			tmax_count = 1
		if tmin_count == 0:
			tmin_count = 1
		if tavg_count == 0:
			tavg_count = 1
		average_tmax = average_tmax / tmax_count
		average_tmin = average_tmin / tmin_count
		average_tavg = average_tavg / tavg_count
		# print( '{0}\t{1}'.format(previous_station_id, average_temperature, previous_day, previous_month, previous_year, aggregation_unit) )
		printData(previous_station_id, previous_day, previous_month, previous_year, aggregation_unit, average_tmax, average_tmin, average_tavg)
		average_tmax, average_tmin, average_tavg = 0, 0, 0
		tmax_count, tmin_count, tavg_count = 0, 0, 0
		printed_station_id = previous_station_id
	
	if type == 'TMAX':
		average_tmax += value
		tmax_count += 1
	elif type == 'TMIN':
		average_tmin += value
		tmin_count += 1
	else:
		average_tavg += value
		tavg_count += 1
	# count += 1
	previous_station_id = current_station_id
	previous_day, previous_month, previous_year = day, month, year

if current_station_id != printed_station_id:
	if tmax_count == 0:
		tmax_count = 1
	if tmin_count == 0:
		tmin_count = 1
	if tavg_count == 0:
		tavg_count = 1

	average_tmax = average_tmax / tmax_count
	average_tmin = average_tmin / tmin_count
	average_tavg = average_tavg / tavg_count
	printData(current_station_id, previous_day, previous_month, previous_year, aggregation_unit, average_tmax, average_tmin, average_tavg)
