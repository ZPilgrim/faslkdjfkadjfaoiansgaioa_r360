#coding = utf8

from parameters import *
import math
from math_utils import *

class Bill:
    def __init__(self, user_id, time=0, bank_id=-1, last_bill=-1, last_payback=-1,
                 credit_limit=-1, this_balance=-1, this_least_pay_back=-1, consume_cnt=-1,
                 this_bill=-1, adjust_bill=-1, loop_interests=-1, repayment=-1,
                 cash_limit = -1 ):
        self.user_id = int(user_id)
        self.time = int(time)
        self.bank_id = bank_id
        self.last_bill = last_bill
        self.last_payback = last_payback
        self.credit_limit = credit_limit
        self.this_balance = this_balance
        self.this_least_pay_back = this_least_pay_back
        self.consume_cnt = consume_cnt
        self.this_bill  = this_bill
        self.adjust_bill = adjust_bill
        self.loop_interests = loop_interests
        self.repayment = repayment
        self.cash_limit = cash_limit


def bill_cmp(a, b):
    if a.time > b.time: return 1
    if a.time < b.time: return -1
    return 0

class User:
    def __init__(self, user_id=-1, loan_time = -1):
        self.user_id = int(user_id)
        self.bills = []
        self.bill_features = []
        self.loan_time = int(loan_time)

    def set_bills(self, bills):
        self.bills = bills
        self.sort_bills()

    def sort_bills(self):
        # sorted(self.bills, cmp=bill_cmp)
        self.bills = sorted(self.bills, cmp=lambda a,b: bill_cmp(a,b))

    def add_bill(self, bill):
        self.bills.append(bill)

    def cal_bill_features(self):

        if len(self.bills)== 0:
            self.bill_features = [default_value for i in range(24)]
            return

        self.sort_bills()

        tot_last_bill = 0.0
        tot_last_payback = 0.0
        tot_this_balance = 0.0
        tot_this_least_payback = 0.0
        tot_consume_cnt = 0
        tot_this_bill = 0.0
        tot_adjust_bill = 0.0
        tot_loop_interests = 0.0
        tot_repayment = 0.0
        dif_this_balance_this_least_payback = []
        big_this_balance_this_least_payback = 0
        dif_repayment_cash_limit = []
        big_repayment_cash_limit = 0

        for b in self.bills:
            tot_last_bill += b.last_bill
            tot_last_payback += b.last_payback
            tot_this_balance += b.this_balance
            tot_this_least_payback += b.this_least_pay_back
            tot_consume_cnt += b.consume_cnt
            tot_this_bill += b.this_bill
            tot_adjust_bill += b.adjust_bill
            tot_loop_interests += b.loop_interests
            tot_repayment += b.repayment

            dif_this_balance_this_least_payback.append( b.this_balance-b.this_least_pay_back )
            if b.this_balance > b.this_least_pay_back : big_this_balance_this_least_payback += 1

            dif_repayment_cash_limit.append( b.repayment - b.cash_limit )
            if b.repayment > b.cash_limit: big_repayment_cash_limit += 1

        big_this_balance_this_least_payback = math.log( 1 + big_this_balance_this_least_payback )
        big_repayment_cash_limit = math.log( 1 + big_repayment_cash_limit )


        b_len = len(self.bills)
        if b_len == 0: b_len = 1
        avg_last_bill = tot_last_bill / b_len
        avg_last_payback = tot_last_payback / b_len
        avg_this_least_payback = tot_this_least_payback / b_len
        avg_this_balance = tot_this_balance / b_len
        avg_consume_cnt = tot_consume_cnt / b_len
        avg_this_bill = tot_this_bill / b_len
        avg_adjust_bill = tot_adjust_bill / b_len
        avg_loop_interests = tot_loop_interests / b_len
        avg_repayment = tot_repayment / b_len


        var_last_bill = 0.0
        var_last_payback = 0.0
        var_this_least_payback = 0.0
        var_this_balance = 0.0
        var_consume_cnt = 0.0
        var_this_bill = 0
        var_adjust_bill = 0
        var_loop_interests = 0
        var_repayment = 0


        for b in self.bills:
            var_last_bill += pow(b.last_bill-avg_last_bill, 2)
            var_last_payback += pow(b.last_payback-avg_last_payback, 2)
            var_this_balance += pow(b.this_balance-avg_this_balance, 2)
            var_this_least_payback = pow(b.this_least_pay_back- avg_this_least_payback, 2)
            var_consume_cnt = pow(b.consume_cnt-avg_consume_cnt, 2)
            var_this_bill = pow( b.this_bill-avg_this_bill, 2 )
            var_adjust_bill = pow( b.adjust_bill-avg_adjust_bill, 2 )
            var_loop_interests = pow( b.loop_interests-avg_loop_interests, 2 )
            var_repayment  = pow( b.repayment-avg_repayment, 2 )

        mean_this_balance_this_least_payback,var_this_balance_this_least_payback =  cal_avg_var(dif_this_balance_this_least_payback)
        mean_repayment_cash_limit, var_repayment_cash_limit = cal_avg_var(dif_repayment_cash_limit)

        self.bill_features += [
            avg_last_bill,var_last_bill,
            avg_last_payback, var_last_payback,
            avg_this_balance, var_this_balance,
            avg_this_least_payback, var_this_least_payback,
            avg_consume_cnt, var_consume_cnt,
            avg_this_bill, var_this_bill,
            avg_adjust_bill, var_adjust_bill,
            avg_loop_interests, var_loop_interests,
            avg_repayment, var_repayment,
            big_this_balance_this_least_payback, big_repayment_cash_limit,
            mean_this_balance_this_least_payback,var_this_balance_this_least_payback,
            mean_repayment_cash_limit, var_repayment_cash_limit,
        ]

        # l = [1265, 3150]
        # if self.user_id in l :
        #     print "fs:", self.bill_features
        #     print "bill_len:", len(self.bills)
        #     print "t:", b.last_bill-avg_last_bill, var_last_bill

    def rerange_bills(self):
        self.sort_bills()
        st = self.loan_time - INTERVAL
        ptr = -1
        for b in self.bills:
            if b.time <= st:
                ptr += 1
            else:
                break
        if ptr == -1: ptr = 0
        self.bills = self.bills[ptr:]

if __name__ == "__main__":
    u = User()
    b1 = Bill( 3, 5 )
    b2 = Bill( 1, 2 )
    u.set_bills([b1, b2])
    for v in u.bills:
        print v.time
