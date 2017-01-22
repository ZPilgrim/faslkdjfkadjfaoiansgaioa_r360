import numpy

def cal_avg_var(nlist):

    narray = numpy.array( nlist )
    mean = narray.sum() / len(nlist)
    return mean, narray.var()
