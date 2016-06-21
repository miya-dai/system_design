import codecs

inputfilename = "2_5_total_strs_descriptors.csv"
outputfilename = "X_all.csv"

inputfile = codecs.open(inputfilename, "r", "utf-8")
lines = inputfile.readlines()
inputfile.close()

outputfile = codecs.open(outputfilename, "w", "utf-8")

del lines[0]
for i, line in enumerate(lines):
	ll = line.split(",")
	string = ""
	string += "%d," % i
	for i, word in enumerate(ll):
		if i == 0 or i == 1:
			continue
		else:
			string += word + ","
	string = string.rstrip(",")
	outputfile.write(string)
outputfile.close()

