import codecs
import numpy as np

normalized_x_all_filename = "normalized_x_all.csv"
cycle_log_filename = "cycle_log.csv"
outputfilename = "euclidean.csv"

ncolumn = 52
ignore_id_column = True

normalized_x_all_file = codecs.open(normalized_x_all_filename, "r", "utf-8")
lines = normalized_x_all_file.readlines()
normalized_x_all_file.close()

normalized_x_data = []
if ignore_id_column is True:
	spacer = 1
else:
	spacer = 0
for line in lines:
	data_row = []
	ll = line.split(",")
	for i in range(spacer, ncolumn + spacer):
		data_row.append(float(ll[i]))
	normalized_x_data.append(np.array(data_row))

cycle_log_file = codecs.open(cycle_log_filename, "r", "utf-8")
lines = cycle_log_file.readlines()
cycle_log_file.close()

ids = []
for line in lines:
	ll = line.split(",")
	ids.append(int(ll[0]))

outputfile = codecs.open(outputfilename, "w", "utf-8")
nids = len(ids)
for i in range(1, nids):
	id_2 = ids[i]
	id_1 = ids[i - 1]
	dist = np.linalg.norm(normalized_x_data[id_2] - normalized_x_data[id_1])
	outputfile.write("%d,%d,%f\n" % (id_1, id_2, dist))
outputfile.close()

