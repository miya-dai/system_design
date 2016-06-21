import numpy as np
import pandas as pd
import sys


arg = sys.argv
x_all = pd.read_csv("x_all.csv", header=None)
y_all = pd.read_csv("y_all.csv", header=None)

sampler = np.random.permutation(len(x_all))

num_of_sample = int(arg[1])
random_num = int(arg[2])
learn_x = x_all.take(sampler[:num_of_sample])
learn_y = y_all.take(sampler[:num_of_sample])

test_x = x_all.take(sampler[num_of_sample:])
test_y = y_all.take(sampler[num_of_sample:])

learn_x.to_csv("./x_csvs/x_%i_%i.csv" %(num_of_sample, random_num), index=False, header=False)
learn_y.to_csv("./y_csvs/y_%i_%i.csv" %(num_of_sample, random_num), index=False, header=False)
test_x.to_csv("./xevals/xeval_%i_%i.csv" %(num_of_sample, random_num), index=False, header=False)
test_y.to_csv("./yevals/yeval_%i_%i.csv" %(num_of_sample, random_num), index=False, header=False)

