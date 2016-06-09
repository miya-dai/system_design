import glob
import sys
import pandas as pd
import shutil

log_dir = "log_datas/"
error_dir = "log_datas/error_datas/"
log_files = glob.glob(str(log_dir) + "*.log")

str_ID_list = []
affinity_list = []
for log_file in log_files:

    f = open(log_file, "r")
    lines = f.readlines()
    f.close()
    try:
        affinity_list.append(float(lines[25][13:17]))
    except:
        print(log_file)
        shutil.move(log_file, error_dir)
    str_ID = log_file.split("/")[1]
    str_ID = str_ID.split("_")[1]
    str_ID = str_ID.split(".")[0]
    str_ID_list.append(str_ID)

sum_log = pd.DataFrame({"affinity":affinity_list, "str_ID":str_ID_list}, columns=['str_ID', 'affinity'])
y = pd.DataFrame({"affinity":affinity_list})
sum_log.to_csv("sum_log.csv")
y.to_csv("y_all.csv", index=False, header=False)