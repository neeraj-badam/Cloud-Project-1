#!/usr/bin/env python3
import sys

args = sys.argv

# Threshold values for heavy rainfall and drought
HEAVY_RAINFALL_THRESHOLD = int( args[1] )  # Adjust threshold value as needed
DROUGHT_THRESHOLD = int( args[2] )  # Adjust threshold value as needed

def printPeriod(station_id, start_date, end_date, period_type):
    print('{0}\t{1}\t{2}\t{3}'.format(station_id, start_date, end_date, period_type))

current_station_id = None
start_date = None
total_precipitation = 0
previous_date = None

for line in sys.stdin:
    station_id, station_date, precipitation = line.strip().split('\t')
    precipitation = float(precipitation)

    if current_station_id and current_station_id != station_id:
        if total_precipitation >= HEAVY_RAINFALL_THRESHOLD:
            printPeriod(current_station_id, start_date, previous_date, 'Heavy Rainfall')
        elif total_precipitation <= DROUGHT_THRESHOLD:
            printPeriod(current_station_id, start_date, previous_date, 'Drought')
        
        # Reset values for the new station
        current_station_id = station_id
        start_date = None
        total_precipitation = 0
    
    current_station_id = station_id
    if not start_date:
        start_date = previous_date
    total_precipitation += precipitation
    previous_date = station_date

# Handle the last station's data
if current_station_id:
    if total_precipitation >= HEAVY_RAINFALL_THRESHOLD:
        printPeriod(current_station_id, start_date, previous_date, 'Heavy Rainfall')
    elif total_precipitation <= DROUGHT_THRESHOLD:
        printPeriod(current_station_id, start_date, previous_date, 'Drought')
