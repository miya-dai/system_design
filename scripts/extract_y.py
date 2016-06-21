import codecs
import glob
import random

protain_name = "3rze"
random_size = 0.001

pdbqt_files = glob.glob("*.sdf.pdb.pdbqt")
log_files = glob.glob("*.log")

structure_ids = [int((pdbqt_file.split("."))[0]) for pdbqt_file in pdbqt_files]

ids_file = codecs.open("structure_ids.csv", "w", "utf-8")
affinity_file = codecs.open("affinity.csv", "w", "utf-8")

for structure_id in structure_ids:
	logfilename = protain_name + "_" + "%d" % structure_id + ".sdf.pdb.pdbqt.log"
	logfile = codecs.open(logfilename, "r", "utf-8")
	logfile_lines = logfile.readlines()
	logfile.close()
	for i, line in enumerate(logfile_lines):
		if line.startswith("-----+------------+----------+----------"):
			affinity_line = logfile_lines[i + 1]
			ll = affinity_line.split(" ")
			while "" in ll:
				ll.remove("")
			affinity = float(ll[1])
			affinity += random_size * (random.random() - 0.5)
			affinity_file.write("%f\n" % affinity)
			ids_file.write("%d\n" % structure_id)
affinity_file.close()
ids_file.close()
