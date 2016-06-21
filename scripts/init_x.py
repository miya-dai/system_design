import codecs

x_all_filename = "X_all.csv"
xeval_filename = "XEval.csv"
x_filename = "X.csv"
structure_ids_filename = "structure_ids.csv"

x_all_file = codecs.open(x_all_filename, "r", "utf-8")
x_all_lines = x_all_file.readlines()
x_all_file.close()

x_entries = {}
for line in x_all_lines:
	ll = line.split(",")
	id = int(ll[0])
	x_entries[id] = line

structure_ids_file = codecs.open(structure_ids_filename, "r", "utf-8")
structure_ids_lines = structure_ids_file.readlines()
structure_ids_file.close()
structure_ids = []
for line in structure_ids_lines:
	structure_ids.append(int(line))

x_file = codecs.open(x_filename, "w", "utf-8")
for id in structure_ids:
	x_file.write(x_entries[id])
x_file.close()

xeval_file = codecs.open(xeval_filename, "w", "utf-8")
for item in x_entries.items():
	id = item[0]
	line = item[1]
	if id in structure_ids:
		continue
	else:
		xeval_file.write(line)
xeval_file.close()

