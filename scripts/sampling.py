import codecs
import random
import subprocess
import glob

nitems = 106770
protain_name = "3rze"

nsample = 100
seed = 20160615

list = [i for i in range(0, nitems)]
random.seed(seed)
random.shuffle(list)

pdbqt_files = glob.glob("pdbqts/*.pdbqt")
config_files = glob.glob("vina_configs/*.config")

counter = 0
for item in list:
	pdbqtname = "pdbqts/%d.sdf.pdb.pdbqt" % item
	configname = "vina_configs/%s_%d.sdf.pdb.pdbqt.config" % (protain_name, item)
	if pdbqtname in pdbqt_files and configname in config_files:
		subprocess.call("cp %s samples/" % pdbqtname, shell = True)
		subprocess.call("cp %s samples/" % configname, shell = True)
		counter += 1
		print(counter)
	if counter == nsample:
		break

