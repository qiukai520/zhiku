# -*- coding: utf-8 -*-
"""
@Author: Lee
@Date  : 2018/11/24 14:58
"""
from django import template
from django.utils.safestring import mark_safe
from ..models import *

register = template.Library()


@register.simple_tag
def fetch_notice_count(user):
    if hasattr(user,"staff"):
        notice_count = user.staff.notice_for_user.filter(notice_status=False).count()
        return notice_count
    return 0



@register.simple_tag
def fetch_notice(user):
    resultdict = {}
    notice_list=[]
    total=0
    if hasattr(user,"staff"):
        notice_list = user.staff.notice_for_user.filter( notice_status=False,).order_by('-notice_time')
        total = notice_list.count()
    data = []
    for notice in notice_list:
        dic = {}
        dic['notice_title'] = notice.notice_title
        dic['notice_body'] = notice.notice_body
        dic['notice_url'] = notice.notice_url
        if notice.notice_status:
            dic['notice_status'] = '已读'
        else:
            dic['notice_status'] = '未读'
        dic['notice_time'] = notice.notice_time
        data.append(dic)
    resultdict['count'] = total
    resultdict['data'] = data
    return resultdict