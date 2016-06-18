import sys
from rdkit import Chem
from rdkit.Chem import AllChem
import glob
import shutil
import os
import multiprocessing as mp

nprocs = 4
except_dir_path = os.path.abspath(os.path.dirname(__file__)) + "\except_mol"

def optimize(mol_file):
	
	try:
		m = Chem.MolFromMolFile(mol_file)
		m = Chem.AddHs(m)
		AllChem.EmbedMolecule(m)
	except:
		shutil.move(mol_file, except_dir_path)
		return
	
	try:
		AllChem.UFFOptimizeMolecule(m)
	except ValueError:
		print("Bad Conformer Id")
		print(mol_file)
		shutil.move(mol_file, except_dir_path)

#	m = Chem.RemoveHs(m)
	w = Chem.SDWriter(mol_file)

	w.write(m)
	print(str(mol_file))
	
	return

if __name__ == "__main__":
	#dir_path = os.path.abspath(os.path.dirname(__file__)) + "\mol_datas"
	mol_files = glob.glob("*.sdf")
	procs = mp.Pool(nprocs)
	procs.map(optimize, mol_files)

