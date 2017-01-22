#encoding=utf-8

def cmp(a,b):
    if a  < b :
        return -1
    else :
        if a > b:
            return 1
        else:
            return 0

list1 = [('david', 90), ('mary',90), ('sara',80),('lily',95)]

print(sorted(list1,cmp = lambda x,y: cmp(x[0],y[0])))#按照第一个位置的字母序排序
#[('david', 90), ('lily', 95), ('mary', 90), ('sara', 80)]

print(sorted(list1,cmp = lambda x,y: cmp(x[1],y[1])))#按照第二个位置的数字序排序

#[('sara', 80), ('david', 90), ('mary', 90), ('lily', 95)]

print cmp("d", "a")