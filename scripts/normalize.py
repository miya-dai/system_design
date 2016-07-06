import sys
import codecs
import numpy as np
from math import sqrt

inputfilename = "X_all.csv"
outputfilename = "normalized_X_all.csv"

ncolumns = 52 # data rows only (does not include ID row)
ignore_id_column = True

inputfile = codecs.open(inputfilename, "r", "utf-8")
lines = inputfile.readlines()
inputfile.close()

ndatas = len(lines)

data_matrix = []
for line in lines:
	data_row = []
	ll = line.split(",")
	spacer = 0
	if ignore_id_column is True:
		spacer = 1
	for i in range(spacer, ncolumns + spacer):
		data_row.append(float(ll[i]))
	data_matrix.append(data_row)

data_matrix = np.matrix(data_matrix)

average = []
for vector in np.transpose(data_matrix):
	average.append(np.mean(vector))

variance = []
for vector in np.transpose(data_matrix):
	variance.append(np.var(np.array(vector)))

stdev = []
for v in variance:
	stdev.append(sqrt(v))

normalized_data_matrix = []
for i in range(ndatas):
	normalized_data_row = []
	for j in range(ncolumns):
		if stdev[j] == 0:
			normalized_data_row.append(0.0)
		else:
			normalized_data_row.append((data_matrix[i, j] - average[j]) / stdev[j])
	normalized_data_matrix.append(normalized_data_row)

normalized_data_matrix = np.matrix(normalized_data_matrix)

outputfile = codecs.open(outputfilename, "w", "utf-8")
for i in range(ndatas):
	string = "%d," % i # ID
	for j in range(ncolumns):
		string += "%f," % normalized_data_matrix[i, j]
	string.rstrip(",")
	string += "\n"
	outputfile.write(string)
outputfile.close()
