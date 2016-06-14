import subprocess as sp
import glob
import multiprocessing as mp

nprocs = 4
pdb2pdbqt_tool_path = "/cygdrive/c/'Program Files (x86)'/MGLTools-1.5.6/Lib/site-packages/AutodockTOols/Utilities24/prepare_ligand4.py"

def pdb2pdbqt(pdbfile):
	sp.call("%s -l %s -o %s" % (pdb2pdbqt_tool_path, pdbfile, pdbfile), shell=True)
	return

if __name__ == "__main__":
	pdbfiles = glob.glob("*.pdb")
	procs = mp.Pool(nprocs)
	procs.map(pdb2pdbqt, pdbfiles)
	