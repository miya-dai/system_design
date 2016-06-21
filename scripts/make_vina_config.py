import sys
import codecs
import glob

file_names = glob.glob("*.pdbqt")

for i, file_name in enumerate(file_names):
	print(i)
	f = codecs.open("3rze_%s.config" %file_name, "w", "utf-8")
	f.write("receptor = 3rze_noLigands.pdbqt\n")
	f.write("ligand = %s\n" %file_name)
	f.write("log = 3rze_%s.log\n" %file_name)
	f.write("\n")
	f.write("center_x = 16.622\n")
	f.write("center_y = 31.995\n")
	f.write("center_z = 24.067\n")
	f.write("\n")
	f.write("size_x = 28\n")
	f.write("size_y = 28\n")
	f.write("size_z = 28\n")
	f.write("\n")
	f.write("cpu = 4\n")
	f.write("seed = 2016\n")
	f.write("\n")
	f.write("num_modes = 100\n")
	f.write("energy_range = 3\n")
	f.close()
	