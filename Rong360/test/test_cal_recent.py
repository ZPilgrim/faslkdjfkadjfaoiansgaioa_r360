from src.bill_features import *

from test.check_case_params import *



if __name__ == "__main__":

    bank_detail_train_df = pd.read_csv(bank_detail_train, header=None, sep=',')
    recent_income, recent_cost = cal_recent_income_cost(bank_detail_train_df, recent_cnt)

    print "income"

    for (k,v) in recent_income.items():
        print (k, v)

    print "cost"

    for (k, v) in recent_cost.items():
        print (k, v)


