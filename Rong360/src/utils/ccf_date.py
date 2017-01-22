# coding: utf-8

import datetime
from src.coupon.parameters import *

def date_diff(d1, d2):
    return (d1 - d2).days

def str_date_diff(d1, d2):
    return (string_to_date(d1) - string_to_date(d2)).days

def string_to_date(str):
    if len(str) < 8:
        return null_date
    else:
        return datetime.date(int(str[0:4]), int(str[4:6]), int(str[6:8]))
