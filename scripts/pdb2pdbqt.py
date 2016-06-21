import subprocess as sp
import glob
import multiprocessing as mp

nprocs = 4
python_path = "/cygdrive/c/'Program Files (x86)'/MGLTools-1.5.6/python.exe"
pdb2pdbqt_tool_path = "C:/'Program Files (x86)'/MGLTools-1.5.6/Lib/site-packages/AutodockTOols/Utilities24/prepare_ligand4.py"

def pdb2pdbqt(pdbfile):
	print(pdbfile)
	sp.call("%s %s -l %s -o %s.pdbqt" % (python_path, pdb2pdbqt_tool_path, pdbfile, pdbfile), shell=True)
	return

if __name__ == "__main__":
	pdbfiles = glob.glob("*.pdb")
	procs = mp.Pool(nprocs)
	procs.map(pdb2pdbqt, pdbfiles)
	