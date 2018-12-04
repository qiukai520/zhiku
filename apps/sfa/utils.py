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
    for key,val in kwargs.items():
        if val:
            filter[key] = val
    return filter


def is_valid_date(str):
    '''判断是否是一个有效的日期字符串'''
    try:
        time.strptime(str, "%Y-%m-%d")
        date = datetime.datetime(str, "%Y-%m-%d")
        print("date",date)
        return str
    except Exception as e:
        print(e)
        print(False)
        return ''


