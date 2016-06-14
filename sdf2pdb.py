import subprocess as sp
import glob
import multiprocessing as mp

nprocs = 4

def sdf2pdb(sdffile):
	sp.call("babel -i sdf %s -o pdb %s.pdb" % (sdffile, sdffile), shell=True)
	return

if __name__ == "__main__":
	sdffiles = glob.glob("*.sdf")
	procs = mp.Pool(nprocs)
	procs.map(sdf2pdb, sdffiles)

