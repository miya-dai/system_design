#!/bin/sh

for txt_file in `\find ./txt_datas -name '*.txt'`; do
	./vina --config $txt_file
done