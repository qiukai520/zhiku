# -*- coding: utf-8 -*-
"""
@Author: Lee
@Date  : 2018/11/30 16:15
"""
import time,datetime

def build_customer_filter(sign,**kwargs):
    filter={}
    if sign < 2:
        filter["sign"]=sign
    print("args",kwargs)
    for key,val in kwargs.items():
        print(val)
        if val:
            filter[key] = val
    return filter


def is_valid_date(str):
    '''判断是否是一个有效的日期字符串'''
    try:
        time.strptime(str, "%Y-%m-%d")
        return str
    except:
        return ''


