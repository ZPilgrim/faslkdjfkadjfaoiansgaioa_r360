
from log import *
from file_io import *
from parameters import *

def change_to_xgb_feature(X, Y, start, add_head = True):
    data = []

    if add_head :
        line = str(0)
        for i in range(0, len(X[0])):
            line += " " + str(i)
        data.append( tuple(line.split(' ')) )

    for j in range(0, len(X)):
        sample = X[j]
        if len(Y) == 0:
            # line = str( random.randint(0, 1) )
            line = str( 1 )
        else:
            line = str(Y[j])

        for i in range(0, len(sample)):
            line += " " + str(start+i) + ":" + str(sample[i])
        d = line.split(' ')
        data.append(tuple(d))

    return data

def predict_by_xgboost(X1, Y1, X2, Y2, prefix,  out_file):
    xgb_train_file = prefix + "xgbtrain_for_predict.csv"
    xgb_test_file = prefix + "xgbtest_for_predict.csv"

    log_info("predict_by_xgboost, X1:" + str(len(X1)) + " Y1:" + str(len(Y1)) + " X2:" + str(len(X2)) )

    data1 = change_to_xgb_feature(X1, Y1, 1, False)
    csv_write_file(xgb_train_file, data1)
    data2 = change_to_xgb_feature(X2, Y2, 1, False)
    csv_write_file(xgb_test_file, data2)

    cnt = 0
    cnt_2 = 0
    for i in range(0, len(Y1)):
        if int( Y1[i] ) == 1:
            cnt += 1
        if i >= len(data2) : continue
        if int(data2[i][0]) == 1:
            cnt_2 += 1
    log_info("xgboost init data end, train rows:" + str(len(data1)) + " col:" + str(len(data1[0])) + " " + str(data1[0]) )
    log_info("train: pos:" + str(cnt) + " neg:" + str(len(Y1) - cnt))
    log_info("test pos:" + str(cnt_2) + " neg:" + str(len(Y2) - cnt_2) + " line:" + str(data2[0]))


    eta = 0.1

    max_depth = 6

    subsample = 0.8

    colsample_bytree = 0.8

    start_time = time.time()

    print('XGBoost params. ETA: {}, MAX_DEPTH: {}, SUBSAMPLE: {}, COLSAMPLE_BY_TREE: {}'.format(eta, max_depth, subsample, colsample_bytree))

    params = {
        "learning_rate" : 0.05,
        "n_estimators":1000,
        "objective": "binary:logistic",

        "booster" : "gbtree",

        # "eval_metric": "auc",

        "eta": eta,

        "max_depth": 6,

        "subsample": subsample,

        "colsample_bytree": colsample_bytree,

        "silent": 1,

        "seed": 0,
    }


    log_info("xgboost read data ")

    dtrain = xgb.DMatrix(xgb_train_file)
    dtest = xgb.DMatrix(xgb_test_file)
    watchlist = [(dtest,'eval'), (dtrain,'train')]
    num_round = 75

    log_info("xgboost start train ")
    bst = xgb.train(params, dtrain, num_round, watchlist)

    log_info("xgboost predict ")
    # by default, we predict using all the trees
    ypred2 = bst.predict(dtest)
    # auc(Y2, ypred2)
    results = []
    predict_samples = sample.get_predict_sample()
    for i in range(len(predict_samples)):
        t = predict_samples[i]
        results.append([t.get(USER_ID), t.get(COUPON_ID), t.get(DATE_RECEIVED), ypred2[i]])

    df = pd.DataFrame(results)
    df.to_csv(output_path_xgb, index=False)

    train_file = prefix + "ccf_offline_stage1_test_revised.csv"
    out_file = prefix + "xgb_raw_out_7_submit.csv"
    write_raw_result_file(ypred2, train_file, out_file)