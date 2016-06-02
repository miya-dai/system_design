#!/bin/sh


for sdf_file in `\find mol_datas/ -name '*.sdf'`; do
	babel -i sdf ${sdf_file} -o pdb ${sdf_file/sdf/pdb}
done

mgl_tools_path="/Library/MGLTools/1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py"

for pdb_file in `\find ./mol_datas -name '*.pdb'`; do
	/Users/DAIKI/Downloads/mgltools_i86Darwin9_1.5.6/bin/pythonsh $mgl_tools_path -l ${pdb_file} -o ${pdb_file/pdb/pdbqt}
done