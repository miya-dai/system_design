#!/bin/python
#! -*- coding: utf-8 -*-

import sys,codecs

inputfilename = "logS_data_set_2D_original.sdf"
idfilename = "logS_mol.sdf"
outputfilename = "logS_data_set.csv"

if __name__ == "__main__":
	
	inputfile = codecs.open(inputfilename, "r", "utf-8")
	inputlines = inputfile.readlines()
	inputfile.close()
	
	idfile = codecs.open(idfilename, "r", "utf-8")
	idlines = idfile.readlines()
	idfile.close()
	
	ids = []
	idflag = False
	for idline in idlines:
		if idline.startswith(">  <ID> "):
			idflag = True
			continue
		if idflag is True:
			ids.append(int(idline))
			idflag = False
			continue
	
	outputfile = codecs.open(outputfilename, "w", "utf-8")
	
	id = -1
	logSflag = False
	for line in inputlines:
		if line.startswith(">  <logS>"):
			logSflag = True
			id += 1
			continue
		if logSflag is True and id in ids:
			outputfile.write(line)
			#outputfile.write("%d,%s" % (id, line))
			logSflag = False
			continue
	
	outputfile.close()
	