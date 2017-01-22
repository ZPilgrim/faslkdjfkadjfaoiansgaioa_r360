#encoding=utf-8

import pandas as pd


def cal_sample_distribution():
    base_dir = "/Users/zhangweimin/Desktop/Rong360/train/"
    overdue_train = base_dir + "overdue_train.csv"
    overdue_train_df = pd.read_csv(overdue_train, header=None, sep=',')
    one_cnt = 0
    zero_cnt = 0
    for v in overdue_train_df.values:
        if int(v[1]) == 0:
            zero_cnt += 1
        else:
            one_cnt += 1

    print "one_cnt:", one_cnt
    print "zero_cnt:", zero_cnt



if __name__ == "__main__":

    train_dir = "/Users/zhangweimin/Desktop/Rong360/train/"
    bank_detail_train_df = pd.read_csv(train_dir+"bank_detail_train.csv", header=None, sep=',')
    print "bank_detail_train:", len( set( bank_detail_train_df[0] ) )

    bill_detail_train_df = pd.read_csv(train_dir + "bill_detail_train.csv", header=None, sep=',')

    sur_list = [ 111 ]

    for v in bill_detail_train_df.values:
        if int(v[0])in sur_list:
            print v


    base_dir = "/Users/zhangweimin/Desktop/Rong360/test/"
    bank_detail_test = base_dir + "bank_detail_test.csv"
    bank_detail_test_df = pd.read_csv(bank_detail_test, header=None, sep=',')

    print "bank_detail:", len( set( bank_detail_test_df[0] ) )



    bill_detail_test = base_dir + "bill_detail_test.csv"
    bill_detail_test_df = pd.read_csv(bill_detail_test, header=None, sep=',')
    print "bill_detail", len( set( bill_detail_test_df[0] ) )

    cal_sample_distribution()
# tot user: 13901