import codecs

inputfilename = "2_5_total_strs.sdf.rename"

inputfile = codecs.open(inputfilename, "r", "utf-8")
input = inputfile.read()
inputfile.close()

inputlines = input.split("$$$$")

for i, line in enumerate(inputlines):
	outputfilename = "%d.sdf" % i
	outputfile = codecs.open(outputfilename, "w", "utf-8")
	line = line.lstrip("\n\n")
	outputfile.write("\n\n\n")
	outputfile.write(line)
	outputfile.write("$$$$\n")
	outputfile.close()
	
