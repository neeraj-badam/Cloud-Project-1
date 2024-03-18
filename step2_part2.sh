#!/bin/bash

successfully_downloaded_files=0
for year in {2024..2024}; do

	cat input/"$year".csv | ./mapper_step2_part2.py state ALASKA ALABAMA "$year"0101 "$year"0131 | ./reducer_step2_part2.py month > output_step2_part2_"$year".txt
	# If we want to print the last 200 lines
	tail -n 200 output_step2_part2_"$year".txt

done

echo "Done program"
for year in {2024..2024}; do
	cat output_step2_part2_"$year".txt >> output_step2_part2.txt
done
