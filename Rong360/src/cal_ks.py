

def cmp(a, b):
    if a < b:
        return -1
    if a > b:
        return 1
    if a == b:
        return 0

def lcmp(a, b):
    if a[0] != b[0]:
        return cmp(a[0], b[0])
    else:
        return cmp(a[1], b[1])


def cal_ks(pre, Y):

    score = []
    zero_cnt = 0
    one_cnt = 0
    ret = 0

    for i in range(len(pre)):
        score.append( [pre[i], Y[i]] )
        if Y[i] == 0:
            zero_cnt += 1
        else :
            one_cnt += 1

    score =  sorted(score,  lcmp)
    # sorted(score, key=lambda s:s[0])
    # print score


    lastv = score[0][0]


    acc_zero = 0.0
    acc_one = 0.0

    for i in range(len(score)):
        s = score[i]
        if lastv != s[0] or i == len(score) - 1:
            lastv = s[0]
            ret = max(ret, abs( acc_zero/zero_cnt - acc_one/one_cnt ))

        if s[1] == 1:
            acc_one += 1
        else:
            acc_zero += 1

    return ret


if __name__ == "__main__":
    pre = [0.8,0.2,0.7,0.3,0.5, 0.5,0.5,0.7,0.7,0.2]
    Y = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, ]

    print cal_ks(pre, Y)