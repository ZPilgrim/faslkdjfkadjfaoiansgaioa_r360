


base_dir = "/Users/zhangweimin/Desktop/Rong360/train/"

base_test_dir = "/Users/zhangweimin/Desktop/Rong360/test/"

INTERVAL = 30000

recent_cnt = 3

#train
bill_detail_train = base_dir + "bill_detail_train.csv"
bank_detail_train = base_dir + "bank_detail_train.csv"
overdue_train = base_dir + "overdue_train.csv"
loan_time_train = base_dir + "loan_time_train.csv"

out_file = base_dir + "out_file.csv"



#test

bill_detail_test = base_test_dir + "bill_detail_test.csv"
bank_detail_test = base_test_dir + "bank_detail_test.csv"
overdue_test = base_test_dir + "overdue_test.csv"
loan_time_test = base_test_dir + "loan_time_test.csv"


submit_out_file = base_test_dir + "submit.csv"

#data file column

#bank_detail
BILL_DETAIL_USERID = 0
BILL_DETAIL_TIMESTAMP = 1
BILL_DETAIL_TRADE_TYPE = 2
BILL_DETAIL_TRADE_AMOUNT = 3
BILL_DETAIL_SALARY_TAG = 4


#bill_detail
BILL_USERID = 0
BILL_TIMESTAMP = 1
BILL_LAST_BILL_AMOUNT = 3
BILL_REPAYMENT_AMOUNT = 4
BILL_CREDIT_LINE = 5


#overdue

OVERDUE_USERID = 0
OVERDUE_RESULT = 1



default_value = -1