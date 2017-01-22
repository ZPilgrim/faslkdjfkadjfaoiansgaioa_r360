
import random

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