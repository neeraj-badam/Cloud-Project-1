#!/bin/bash

successfully_downloaded_files=0
for year in {2000..2024}; do

	hadoop fs -put "input/$year.csv" "/input/$year.csv"

	mapred streaming -files mapper_step1.py,reducer_step1.py -mapper 'mapper_step1.py' -reducer reducer_step1.py -input "/input/$year.csv" -output "/input_clean_data/$year.csv"
	
	hdfs dfs -copyToLocal "/input_clean_data/$year.csv/part-00000" "input_clean/$year.csv"
	
	# To print if we want to see the data
	# cat "input_clean/$year.csv"

done
