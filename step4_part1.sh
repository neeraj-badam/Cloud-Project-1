#!/bin/bash

successfully_downloaded_files=0
for year in {2024..2024}; do

	cat input_clean/"$year".csv | ./mapper_step4_part1.py state ALASKA "$year"0101 "$year"0131 | ./reducer_step4_part1.py month > output_step4_part1_"$year".txt
	# If we want to print the last 200 lines
	tail -n 200 output_step4_part1_"$year".txt


done

for year in {2024..2024}; do
	cat output_step4_part1_"$year".txt >> output_step4_part1.txt
done
