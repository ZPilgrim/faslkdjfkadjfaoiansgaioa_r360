from src.bill_features import *

from test.check_case_params import *



if __name__ == "__main__":
    bank_detail_train_df = pd.read_csv(bank_detail_train, header=None, sep=',')
    bill_detail_train_df = pd.read_csv(bill_detail_train, header=None, sep=',')
    overdue_train_df = pd.read_csv(overdue_train, header=None, sep=',')


    recent_income, recent_cost = cal_recent_income_cost(bank_detail_train_df, recent_cnt)
    bill_features_dict, feature_cnt = cal_bill_features_dict(bill_detail_train_df, recent_income, recent_cost)

    X, Y = process_samples(overdue_train_df, bill_features_dict, feature_cnt)

    for (k, v) in bill_features_dict.items() :
        print k, v

    write_file(X, Y)