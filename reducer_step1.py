#!/usr/bin/env python3
import sys
from datetime import datetime, timedelta

def handleTemperatureOutliers(data, index):
	total_value = 0
	if index > 3 and index < (total_records - 4):
		count1 = 0
		while count1 < 3 and index > 0:
			current_station_id, current_date, type, value = records[index].split('\t')
			if type != 'PRCP':
				total_value += int( value )
			index -= 1
			count1 += 1
		count2 = 0
		while count2 < 3 and index < (total_records - 4):
			current_station_id, current_date, type, value = records[index].split('\t')
			if type != 'PRCP':
                                total_value += int( value )
			index += 1
			count2 += 1
	if total_value != 0:
		return total_value / ( count1 + count2 )
	else:
		return None

def printData(include_station_data):
	for data in include_station_data:
		type, value = data['type'], int(data['value'])
		if value == '':
			if type == 'TAVG' and previous_tmax and previous_tmin:
				value = (previous_tmax + previous_tmin) / 2
			elif type == 'TMIN' and previous_tmax and previous_tavg:
				value = 2 * previous_tavg - previous_tmax
			elif type == 'TMAX' and previous_tmax and previous_tavg:
				value = 2 * previous_tavg - previous_tmin
			else:
				value = sum( previous_prcp )
		elif type == 'TMAX':
			if value > 80:
				result = handleTemperatureOutliers(include_station_data, data['index'])
				if result:
					value = result
			previous_tmax = value
		elif type == 'TMIN':
			if value > 50:
				result = handleTemperatureOutliers(include_station_data, data['index'])
				if result:
					value = result
			previous_tmin = value
		elif type == 'TAVG':
			if value > 70:
				result = handleTemperatureOutliers(include_station_data, data['index'])
				if result:
					value = result
			previous_tavg = value
		else:
			# Handling precipitation outliers
			if value > 50:
				value = sum( previous_prcp )
			previous_prcp.append( value )
			if  len( previous_prcp ) >= 3:
				previous_prcp.pop()
		print( '{0},{1},{2},{3}'.format(data['station_id'], data['date'], data['type'], value ) )


previous_tmax, previous_tmin, previous_tavg, previous_prcp = None, None, None, []
previous_station_id, previous_date = None, None
missing_count = None
temperature_data = { 'TMAX': None, 'TMIN': None, 'TAVG': None, 'PRCP': None }
exclude_station_id = False
include_station_data = []
records = []

for line in sys.stdin:
	records.append( line )
total_records = len( records )

for index in range(total_records) :

	current_station_id, current_date, type, value = records[index].split('\t')
	value = int(value)

	if previous_station_id and current_station_id != previous_station_id:
		if not exclude_station_id:
			printData( include_station_data )
		missing_count = 0
		exclude_station_id = False
		include_station_data = []
		previous_tmax, previous_tmin, previous_tavg, previous_prcp = None, None, None, []
	if previous_date and current_date != datetime.strptime(previous_date,'%Y%m%d') + timedelta(days=1):
		missing_count = 0
	if value or value == 0:
		missing_count = 0
		temperature_data[type] = value
	else:
		missing_count += 1

	if missing_count > 10:
		exclude_station_id = True

	if not exclude_station_id:
		include_station_data.append({'station_id': current_station_id, 'date': current_date, 'type': type, 'value':  value, 'index': index })

	previous_station_id = current_station_id
	previous_date = current_date

if not exclude_station_id:
	printData( include_station_data )
