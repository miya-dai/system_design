import numpy as np
import pandas as pd
import sys

arg = sys.argv
x_all = pd.read_csv("x_all.csv", header=None)
y_all = pd.read_csv("y_all.csv", header=None)

sampler = np.random.permutation(len(x_all))

num_of_sample = int(arg[1])
learn_x = x_all.take(sampler[:num_of_sample])
learn_y = y_all.take(sampler[:num_of_sample])

test_x = x_all.take(sampler[num_of_sample:])
test_y = y_all.take(sampler[num_of_sample:])

learn_x.to_csv("x.csv", index=False, header=False)
learn_y.to_csv("y.csv", index=False, header=False)
test_x.to_csv("xeval.csv", index=False, header=False)
test_y.to_csv("yeval.csv", index=False, header=False)