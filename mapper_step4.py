#!/usr/bin/env python3
import sys
from datetime import datetime

for line in sys.stdin:
	fields = line.strip().split(',')
	station_id = fields[0]
	date = datetime.strptime(fields[1], '%Y%m%d')
	type = fields[2]
	precipitation = float(fields[3])

	# Emit station ID and precipitation value
	if type == 'PRCP':
		print('{0}\t{1}\t{2}'.format(station_id, date, precipitation))
