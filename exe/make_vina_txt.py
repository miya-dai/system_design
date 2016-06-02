import sys
import glob

search_dir = "/Users/DAIKI/workspace/class/System_design/exe/mol_datas"
pdbqt_files = glob.glob(str(search_dir)+"/*.pdbqt")

for pdbqt_file in pdbqt_files:
	file_name = pdbqt_file.split("/")[8]
	file_name = file_name.strip(".pdbqt")
	f = open("txt_datas/3rze_%s.txt" %file_name, "w")
	f.write("receptor = 3rze_noLigands.pdbqt\n")
	f.write("ligand = mol_datas/%s.pdbqt\n" %file_name)
	f.write("log = log_datas/3rze_%s.log\n" %file_name)
	f.write("\n")
	f.write("center_x = 16.622\n")
	f.write("center_y = 31.995\n")
	f.write("center_z = 24.067\n")
	f.write("\n")
	f.write("size_x = 28\n")
	f.write("size_y = 28\n")
	f.write("size_z = 28\n")
	f.write("\n")
	f.write("cpu = 2\n")
	f.write("seed = 1000\n")
	f.write("\n")
	f.write("num_modes = 100\n")
	f.write("energy_range = 3\n")
	f.close()