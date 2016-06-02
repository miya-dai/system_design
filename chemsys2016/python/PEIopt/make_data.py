import pandas as pd
import numpy as np
import sys


def make_ID_container():
## 構造記述子が計算されている構造IDを抽出
	y_data_search = open ("logS_mol.sdf", "r")
	container_list = []
	b = 0
	container_list.append([])
	for line in y_data_search: 
	    container_list[b].append(line)
	    if "$$$$" in line:
	        b += 1
	        container_list.append([]) 
	        continue
	ID_container = []
	for i in range(len(container_list)-1):
	    for line in container_list[i]:
	        if "<ID>" in line:
	            num = container_list[i].index(line)
	    ID = int(container_list[i][num+1].strip("\n"))
	    ID_container.append(ID)
	return(ID_container)

def extract_mod_data(structure_IDs):
# オリジナルデータから構造記述子データがあるもののみ抽出
	y_data = open("logS_data_set_2D_original.sdf", "r")
	ori_container = []
	a = 0
	for line in y_data:
		ori_container.append([])
		ori_container[a].append(line)
		if "$$$$" in line:
			a += 1
			continue

	mod_container = []
	for ID in structure_IDs:
		mod_container.append(ori_container[ID])

	return(mod_container)

def extract_logS(learn_x, mod_data):
# データからlogSデータを抽出

	learn_y_list = []
	for ID in learn_x.index:
	    search_num = mod_data[ID].index(">  <logS>\n")
	    log_S = mod_data[ID][search_num + 1].strip("\n")
	    learn_y_list.append(float(log_S))

	return(learn_y_list)

def del_dup_data(learn_x,learn_y):
## yが重複したデータを削除
	x_list_uniq = []
	y_list_uniq = []
	for i in zip(learn_x,learn_y):
	    if i[1] not in y_list_uniq:
	        x_list_uniq.append(i[0])
	        y_list_uniq.append(i[1])
	y_log_df = pd.DataFrame(y_list_uniq)
	return(y_log_df)



# 学習用データとして取り出したい個数を指定
arg = sys.argv

logs_mcd = pd.read_csv("logS_mcd.csv") 
sampler = np.random.permutation(len(logs_mcd))


y_data = pd.read_csv("logS_data_set.csv",header = None)
y_data_search = open ("logS_mol.sdf", "r")

y_data = list(y_data.values.flatten())

structure_IDs = make_ID_container()
mod_data = extract_mod_data(structure_IDs)

if str(arg[1]) == "csv":
	num_of_sample = int(arg[2])
	learn_x = logs_mcd.take(sampler[:num_of_sample])
	test_x = logs_mcd.take(sampler[num_of_sample:])
	learn_y = extract_logS(learn_x, mod_data)

	y_log_df = del_dup_data(learn_x,learn_y)

	y_log_df.to_csv("y_logS_%d.csv" %num_of_sample, header = None, index = None)
	learn_x = learn_x.ix[:,2:]
	test_x = test_x.ix[:,2:]
	learn_x.to_csv("x_%d.csv" %num_of_sample, header = None, index = None)
	test_x.to_csv("xeval_%d.csv" %num_of_sample, header = None, index = None)
	test_x_structure = test_x.ix[:,0:1]

if str(arg[1]) == "sdf":
	# data to sdf
	f = open("logS_data_set_2D_selected.sdf", "w")
	for i in range(len(mod_data)):
		for j in range(len(mod_data[i])):
			f.write(mod_data[i][j])
	print(len(mod_data))
	for div_i in range(len(mod_data)):
	
		search_num = mod_data[div_i].index(">  <CA_Number>\n")
		file_name = mod_data[div_i][search_num + 1].strip("\n")
		

		file_name = file_name.strip()
		div_file = open("./mol_datas/%s.sdf" % file_name,"w")
		for data_line in range(len(mod_data[div_i])):
			div_file.write(mod_data[div_i][data_line])
		div_file.close()

	f.close()

y_data_search.close()

