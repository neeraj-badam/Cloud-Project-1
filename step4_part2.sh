#!/bin/bash

successfully_downloaded_files=0
for year in {2000..2024}; do

	cat input_clean/"$year".csv | ./mapper_step4.py | ./reducer_step4.py 10 50 > output_step4_part2_"$year".txt
	# If we want to print the last 200 lines
	tail -n 200 output_step4_part2_"$year".txt


done

for year in {2000..2024}; do
	cat output_step4_part2_"$year".txt >> output_step4_part2.txt
done
