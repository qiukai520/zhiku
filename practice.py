# -*- coding: utf-8 -*-
'''
@File  : practice.py
@Author: Lee
@Date  : 2018/11/7 10:21
'''

__author__ = 'lizhihong'

#独立使用django的model
import sys
import os

pwd = os.path.dirname(os.path.abspath(__file__))

sys.path.append(pwd+"../")
# 加载配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thinking_library.settings")

import django
django.setup()


