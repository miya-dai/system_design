#!/bin/sh

for sample_num in 10 20 30 40 50; do
	for random_num in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do
		python make_model_data.py $sample_num $random_num
	done
done