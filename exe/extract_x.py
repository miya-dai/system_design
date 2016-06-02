import pandas as pd

y_data = open ("logS_data_set_2D_selected.sdf", "r")
ori_container = []
a = 0
for line in y_data:
	ori_container.append([])
	ori_container[a].append(line)
	if "$$$$" in line:
		a += 1
		continue

y_source = pd.read_csv("sum_log.csv")

x_source = pd.read_csv("logS_mcd.csv")

str_num_list = []
for cas_ID in y_source["str_ID"]:
    search_str = str(cas_ID)+"\n"
    for sdf in ori_container:
        if search_str in sdf:
            str_num = ori_container.index(sdf)
    str_num_list.append(int(str_num))
    str_num_list.sort()

for str_num in str_num_list:
    x = pd.DataFrame(x_source.ix[str_num,2:])

x_list = []
for str_num in str_num_list:
    x_list.append(x_source.ix[str_num,2:].values.flatten())
    
x = pd.DataFrame(x_list)
x.to_csv("x_all.csv", index=False, header=False)