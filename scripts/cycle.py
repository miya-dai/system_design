import codecs
import subprocess
import random

ncycles = 10
seed = 19940727
random_size = 0.001
random.seed(seed)

structure_ids_filename = "structure_ids.csv"
y_filename = "y.csv"
x_filename = "X.csv"
xeval_filename = "XEval.csv"
result_filename = "result.csv"
gp_script_name = "PEIOPT_edit.py"
protein_name = "3rze"

def choose_and_simulate(counter):
	
	subprocess.call("rename result.csv result.%d.csv" % counter, shell = True) # cmd.exe
	subprocess.call("rm result.csv", shell = True)
	subprocess.call("python %s" % gp_script_name, shell = True)
	result_file = codecs.open(result_filename, "r", "utf-8")
	result_lines = result_file.readlines()
	result_file.close()
	result_line = result_lines[1]
	result_ll = result_line.split(",")
	next_entry_linenum = None
	for i, word in enumerate(result_ll):
		if word == "id":
			next_entry_linenum = int(result_ll[i + 1])
	
	xeval_entries = {}
	xeval_file = codecs.open(xeval_filename, "r", "utf-8")
	xeval_lines = xeval_file.readlines()
	xeval_file.close()
	next_entry_id = None
	for i, xeval_line in enumerate(xeval_lines):
		words = xeval_line.split(",")
		id = int(words[0])
		xeval_entries[id] = xeval_line
		if i == next_entry_linenum:
			next_entry_id = id
	
	pdbqt_filename = "%d.sdf.pdb.pdbqt" % next_entry_id
	config_filename = "%s_%d.sdf.pdb.pdbqt.config" % (protein_name, next_entry_id)
	subprocess.call("cp pdbqts/%s cycle/%s" % (pdbqt_filename, pdbqt_filename), shell = True)
	subprocess.call("cp vina_configs/%s cycle/%s" % (config_filename, config_filename), shell = True)
	subprocess.call("cd cycle & vina.exe --config %s_%d.sdf.pdb.pdbqt.config & cd ../" % (protein_name, next_entry_id), shell = True)
	
	last_entry_id = next_entry_id

	x_file = codecs.open(x_filename, "a", "utf-8")
	xeval_file = codecs.open(xeval_filename, "w", "utf-8")
	for item in xeval_entries.items():
		id = item[0]
		entry = item[1]
		if id == last_entry_id:
			x_file.write(entry)
		else:
			xeval_file.write(entry)
	x_file.close()
	xeval_file.close()
	
	y_file = codecs.open(y_filename, "a", "utf-8")
	log_filename = "%s_%d.sdf.pdb.pdbqt.log" % (protein_name, next_entry_id)
	subprocess.call("cp cycle/%s %s" % (log_filename, log_filename), shell = True)
	log_file = codecs.open(log_filename, "r", "utf-8")
	logfile_lines = log_file.readlines()
	log_file.close()
	for i, line in enumerate(logfile_lines):
		if line.startswith("-----+------------+----------+----------"):
			affinity_line = logfile_lines[i + 1]
			ll = affinity_line.split(" ")
			while "" in ll:
				ll.remove("")
			affinity = float(ll[1])
			affinity += random_size * (random.random() - 0.5)
			y_file.write("%f\n" % affinity)
	y_file.close()



if __name__ == "__main__":
	
	for i in range(ncycles):
		choose_and_simulate(i)
