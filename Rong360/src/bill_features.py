#encoding=utf-8

import pandas as pd
import math
from parameters import *
from file_io import *
from cal_ks import *
from log import *
from sklearn.ensemble import GradientBoostingClassifier
from User import *

class Recent_Bill:
    def __init__(self, id, cnt):
        self.id = id
        self.recent_cnt = cnt
        self.incomes = []
        self.cost = []

    def get_recent_incomes(self):
        return self.incomes

    def get_recent_outcomes(self):
        return self.cost

    def get_tot_recent_incomes(self):
        return sum(self.incomes)

    def get_tot_recent_cost(self):
        return sum(self.cost)



#cnt:最近几次的
def cal_recent_income_cost(df, cnt):
    recent_income = {} #userid:recnt_bill
    recent_cost = {}

    df.sort([BILL_DETAIL_USERID, BILL_DETAIL_TIMESTAMP, BILL_DETAIL_TRADE_TYPE, BILL_DETAIL_SALARY_TAG])
    # print df.values
    all_user_id = set(df[BILL_DETAIL_USERID])

    last_v = -1
    for v in all_user_id:
        if v != last_v:

            last_v =  v

            user_record_df = df.loc[ df[BILL_DETAIL_USERID] == v ]

            # user_income_records = user_record_df.loc[ user_record_df[BILL_DETAIL_TRADE_TYPE] == 0 ].values
            # user_cost_records = user_record_df.loc[ user_record_df[BILL_DETAIL_TRADE_TYPE] == 1 ].values

            user_income_records = []
            user_cost_records = []

            for r in user_record_df.values:

                if r[BILL_DETAIL_TRADE_TYPE] == 0:
                    user_income_records.append(r[BILL_DETAIL_TRADE_AMOUNT])
                else :
                    user_cost_records.append(r[BILL_DETAIL_TRADE_AMOUNT])

            if len(user_cost_records) == 0:
                recent_income[v] = 0
                recent_cost[v] = 0
                continue

            tot_income = 0.0 #sum(user_income_records)

            if len(user_income_records) < cnt:
                if len(user_income_records) != 0:
                    tot_income = sum(user_income_records) * cnt * 1.0 / len(user_income_records)
            else:
                tot_income = sum(user_income_records[ (len(user_income_records) - cnt): ]  )

            tot_cost = 0.0 #sum(user_cost_records)
            if len(user_cost_records) < cnt :
                if len(user_income_records) > 0 :
                    tot_cost = sum(user_cost_records) * cnt * 1.0 / len(user_cost_records)
            else:
                tot_cost = sum( user_cost_records[(len(user_cost_records) - cnt):] )

            recent_income[v] = tot_income
            recent_cost[v] = tot_cost

    return recent_income, recent_cost

def cal_bill_features_dict(df, recent_income, recent_cost, bill_user_dict, part_cnt ):

    df.sort( [BILL_USERID, BILL_TIMESTAMP ] )


    all_user_ids = set( df[BILL_USERID] )
    feature_dict  = {}

    default_part_features = [ default_value for i in range(part_cnt)]

    for id in all_user_ids:

        user_records = df.loc[ df[ BILL_USERID ] == id ].values
        bigger = 0
        less = 0

        tot_bill_amount = 0.0
        tot_bill_repay = 0.0


        for r in user_records:
            if r[BILL_LAST_BILL_AMOUNT] > r[BILL_REPAYMENT_AMOUNT]:
                bigger += 1
                # print "a,b:", r[BILL_LAST_BILL_AMOUNT] , r[BILL_REPAYMENT_AMOUNT]
            else:
                less += 1
            tot_bill_amount += r[BILL_LAST_BILL_AMOUNT]
            tot_bill_repay += r[BILL_REPAYMENT_AMOUNT]

        bigger = max(1, bigger)
        less =  max(1, less)

        feature_dict[id] = []

        if bill_user_dict.has_key(id):
            feature_dict[id] += bill_user_dict[id]
        else:
            feature_dict[id] += default_part_features

        feature_dict[id].append( math.log( bigger ) )
        feature_dict[id].append( math.log(less) )

        # print "id, bigger, less:", id, bigger, less

        default_income = 0
        default_cost = 0

        if recent_income.has_key(id):
            feature_dict[id].append(recent_income[id])
        else:
            feature_dict[id].append(default_income)

        if recent_cost.has_key(id):
            feature_dict[id].append( recent_cost[id] )
        else:
            feature_dict[id].append( default_cost)

        feature_dict[id].append( tot_bill_amount )
        feature_dict[id].append( tot_bill_repay )

        if len(user_records) != 0:
            feature_dict[id].append( tot_bill_repay/len(user_records) )
            feature_dict[id].append( tot_bill_amount/len(user_records) )
        else :
            feature_dict[id].append( 0 )
            feature_dict[id].append( 0 )

        feature_cnt = len(feature_dict[id])

    return feature_dict, feature_cnt


def process_samples(df, dic, feature_cnt):

    default_feature = [0 for i in range(feature_cnt)]

    ret = []
    Y = []

    for r in df.values:
        if dic.has_key(r[OVERDUE_USERID]):
            ret.append(dic[ r[OVERDUE_USERID] ])
        else :
            ret.append( default_feature )

        Y.append(r[OVERDUE_RESULT])


    return ret, Y


def process_test_samples(df, dic, feature_cnt):

    default_feature = [default_value for i in range(feature_cnt)]

    ret = []


    for r in df.values:
        if dic.has_key(r[OVERDUE_USERID]):
            ret.append(dic[ r[OVERDUE_USERID] ])
        else :
            ret.append( default_feature )

        # Y.append(r[OVERDUE_RESULT])


    return ret

def write_file(X, Y, out_file):

    result = []

    for i in range(len(X)):
        result.append( Y[i] + X[i] )

    csv_write_file(out_file, result)

# user_idx  user_id : users's idx
def cal_bill_user_dict(users, bill_detail_df, user_idx):

    log_info("--> cal_bill_user_dict")

    bill_user_dict = {}

    bill_details = bill_detail_df.values

    for i in range(len(bill_details)):
        userid = int( bill_details[i][0] )
        time = int( bill_details[i][1] )
        bank_id = int( bill_details[i][2] )
        last_bill = float( bill_details[i][3] )
        last_payback = float( bill_details[i][4] )
        credit_limit = float( bill_details[i][5] )
        this_balance = float( bill_details[i][6] )
        this_least_pay_back = float( bill_details[i][7] )
        consume_cnt = int( bill_details[i][8] )
        this_bill = float( bill_details[i][9] )
        adjust_bill = float( bill_details[i][10] )
        loop_interests = float( bill_details[i][11] )
        repayment = float( bill_details[i][12] )

        b = Bill( userid, time, bank_id, last_bill, last_payback, credit_limit,
                  this_balance, this_least_pay_back, consume_cnt, this_bill,
                  adjust_bill, loop_interests, repayment)

        if user_idx.has_key( userid ) == False :
            user_idx[userid] = User()
        users[ user_idx[ userid ] ].add_bill( b )

    for u in users:
        u.rerange_bills()
        u.cal_bill_features()
        bill_user_dict [u.user_id] = u.bill_features

    log_info("<-- cal_bill_user_dict")

    return bill_user_dict, len( users[0].bill_features )

def init_users(loan_time_df):

    vs = loan_time_df.values
    users = []
    user_index = {}

    log_info("--> init users")
    for v in vs:
        u = User( int(v[0]), int(v[1]) )
        user_index[ u.user_id ] = len(users)
        users.append(u)
    log_info("<-- init users")

    return users, user_index



def test_gbdt(X1, Y1, X2, Y2=[]):
    log_info("gbdt training...")
    clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.05, max_depth = 6, random_state = 0).fit(X1, Y1)
    log_info("gbdt predicting...")
    pre = clf.predict_proba(X2)
 #   log_info("tyoe pre[1]" + str(type(pre[0][1])) + " " + str(pre[0][1]))
    pre = [float(i[1]) for i in pre]
    log_info("offline test," + str( len(pre) ) + " , " + str( len(Y2) ))
    ks = -1
    if len(Y2) == len(pre):

        ks  = cal_ks(pre, Y2)
    print "ks:", ks

    return pre

def combine_X(X, filea):
    ret = []
    Y = []
    filea_values = pd.read_csv(filea, header=None, sep=',').values

    log_info("conbine:" + str( len(X) ) + " , " + str( len(filea_values) ) )

    for i in range(len(filea_values)):
        v = X[i]+ list(filea_values[i][1:])
        try:
            ret.append( [float(c) for c in v] )
        except Exception,e:
            print Exception, e
            print "v:", filea_values[i][1:]

        Y.append( float( filea_values[i][0] ) )

    print "Y[0]:", Y[0]

    return ret, Y

def offline_test(X, Y):
    cut = len(X)/5*4
    print "X[0], Y[0]:", X[0], Y[0]
    test_gbdt(X[0:cut], Y[0:cut], X[cut:], Y[cut:])

def train():
    bank_detail_train_df = pd.read_csv(bank_detail_train, header=None, sep=',')
    bill_detail_train_df = pd.read_csv(bill_detail_train, header=None, sep=',')
    overdue_train_df = pd.read_csv(overdue_train, header=None, sep=',')
    loan_time_train_df = pd.read_csv(loan_time_train, header=None, sep=',')

    users, user_index = init_users(loan_time_train_df)
    bill_user_dict, part_cnt = cal_bill_user_dict(users, bill_detail_train_df, user_index)


    recent_income, recent_cost = cal_recent_income_cost(bank_detail_train_df, recent_cnt)
    bill_features_dict, feature_cnt = cal_bill_features_dict(bill_detail_train_df, recent_income, recent_cost, bill_user_dict, part_cnt)


    X, Y = process_samples(overdue_train_df, bill_features_dict, feature_cnt)
    write_file(X, Y, out_file)

    return X,Y

def test():
    bank_detail_test_df = pd.read_csv(bank_detail_test, header=None, sep=',')
    bill_detail_test_df = pd.read_csv(bill_detail_test, header=None, sep=',')
    loan_time_test_df = pd.read_csv(loan_time_test, header=None, sep=',')

    users, user_index = init_users(loan_time_test_df)
    bill_user_dict, part_cnt = cal_bill_user_dict(users, bill_detail_test_df, user_index)

    recent_income, recent_cost = cal_recent_income_cost(bank_detail_test_df, recent_cnt)
    bill_features_dict, feature_cnt = cal_bill_features_dict(bill_detail_test_df, recent_income, recent_cost, bill_user_dict, part_cnt)

    X = process_test_samples(loan_time_test_df, bill_features_dict, feature_cnt)
    # write_file(X, Y, submit_out_file)
    X, ids = combine_X(X, base_test_dir + "pro_user_info_test.csv" )

    return X, ids

def predict(X, Y, X2, ids, submit_file):

    pre = test_gbdt(X, Y, X2)

    ret = [  ]


    print "ids[i], pre[i],", ids[0], pre[0]

    for i in range(len(pre)):
        ret.append( [ int(ids[i]), pre[i], ] )

    df = pd.DataFrame(ret)
    df.to_csv(submit_file, header=["userid", "probability"], index=None)

if __name__ == "__main__" :

    X, Y = train()
    X, id1 = combine_X(X, base_dir + "pro_user_info_train.csv")
    offline_test(X, Y)

    X2, ids = test()

    predict(X, Y, X2, ids, submit_out_file)

