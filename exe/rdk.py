import sys
from rdkit import Chem
from rdkit.Chem import AllChem
import glob
import shutil


dir_path = "/Users/DAIKI/workspace/class/System_design/exe/mol_datas/"
except_dir_path = "/Users/DAIKI/workspace/class/System_design/exe/except_mol/"
mol_files = glob.glob(str(dir_path)+"*sdf")
for mol_file in mol_files:
	m = Chem.MolFromMolFile(mol_file)
	m = Chem.AddHs(m)
	AllChem.EmbedMolecule(m)
	
	try:
		AllChem.UFFOptimizeMolecule(m)
	except ValueError:
		print("Bad Conformer Id")
		print(mol_file)
		shutil.move(mol_file, except_dir_path)

#	m = Chem.RemoveHs(m)
	w = Chem.SDWriter(mol_file)

	w.write(m)


