#!/usr/bin/env python3
import sys

for line in sys.stdin:
	fields = line.strip().split(',')
	station_id = fields[0]
	country_code = station_id[:2]
	type = fields[2]
	if country_code[:2] in ['US','CA','MX'] and type in ['TMAX', 'TMIN', 'TAVG', 'PRCP']:
		print( '{0}\t{1}\t{2}\t{3}'.format( station_id, fields[1], fields[2], fields[3] ) )
