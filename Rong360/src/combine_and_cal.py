
import pandas as pd
from parameters import *

def combine_files(filea, fileb):
    ret = []
    filea_values = pd.read_csv(filea, header=None, sep=',').values
    fileb_values = pd.read_csv(fileb, header=None, sep=',').values
    for i in range(len(filea_values)):
        ret.append([filea_values[i], fileb_values[i][1:], ])
    return ret

def train(X, Y, X2):

    pass

def train_and_cal():

    filea = out_file
    fileb = base_dir + "pro_user_info_train.csv"
    out = combine_files(filea, fileb)

    result = train()

    df = pd.DataFrame(result)
    df.to_csv(submit_out_file)
