import json
import calendar
import datetime
from datetime import timedelta


def build_tags_info(dict, tags):
    tags_list = []
    for item in tags:
        tag_dict = {"name": item}
        tag_dict.update(dict)
        tags_list.append(tag_dict)
    return tags_list


def build_assign_tags_info(tasid,tags):
    tags_list = []
    for item in tags:
        tag_dict = {"tasid_id": tasid, "name": item}
        tags_list.append(tag_dict)
    return tags_list


def build_attachment_info(id_dict, attachment_list):
    att_list = []
    for item in attachment_list:
        item.update(id_dict)
        att_list.append(item)
    return att_list


def build_assign_attach_info(tasid,attachment):
    att_list = []
    attachment = json.loads(attachment)
    for item in list(attachment):
        item.update({"tasid_id": tasid})
        att_list.append(item)
    return att_list


def build_reviewer_info(tmid, reviewers):
    re_list = []
    reviewers = json.loads(reviewers)
    for item in list(reviewers):
        item.update({"timd_id": tmid})
        re_list.append(item)
    return re_list




def build_statistic_filter(dpid,sid,first_day,last_day):
    filter={}
    filter['first_day'],filter["last_day"]=first_day,last_day
    if int(sid) != 0:
        filter["sid"] = sid
    elif int(dpid) != 0:
        filter["dpid"] = dpid
    return filter


def getMonthFirstDayAndLastDay(startMonth,endMonth):
    """
    :param year: 年份，默认是本年，可传int或str类型
    :param month: 月份，默认是本月，可传int或str类型
    :return: firstDay: 开始月的第一天，datetime.date类型
              lastDay: 结束月的最后一天，datetime.date类型
    """
    start_year, start_month = str(startMonth).split("-")
    end_year, end_month = str(endMonth).split("-")
    if start_year:
        start_year = int(start_year)
    else:
        start_year = datetime.date.today().year
    if start_month:
        start_month = int(start_month)
    else:
        start_month = datetime.date.today().month
    if end_year:
        end_year = int(end_year)
    else:
        end_year = datetime.date.today().year
    if end_month:
        end_month = int(end_month)
    else:
        end_month = datetime.date.today().month
    # 获取endMonth第一天的星期和当月的总天数
    firstDayWeekDay, monthRange = calendar.monthrange(end_year, end_month)
    # 获取strtMonth的第一天
    firstDay = datetime.date(year=start_year, month=start_month, day=1)
    # 获取endMonth的第一天
    lastDay = datetime.date(year=end_year, month=end_month, day=monthRange)

    return firstDay, lastDay


def calculate_deadline(cycle_id, deadline, start_time=None):
    """
    根据项目截止时间与周期，计算每次任务的开始时间与截止时间
    :param cycle_id: 任务周期id
    :param start_time: 开始时间
    :param deadline: 截止时间
    :return:start_time,deadline
    """
    # 查看任务周期
    # 如果是每天任务
    if not start_time:
        start_time = datetime.datetime.today()
    else:
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")

    if int(cycle_id) == 1:
        # 单次任务
        pass

    elif int(cycle_id) == 2:
        # 每天任务
        now = datetime.datetime.today()
        deadline = start_time - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
        deadline += timedelta(hours=18)
        deadline = deadline.strftime("%Y-%m-%d %H:%M")
    elif int(cycle_id) == 3:
        # 每周任务
        weekday = start_time.weekday()
        target_day = calendar.FRIDAY
        del_day = target_day-weekday
        now = datetime.datetime.today()
        start_time_zero = start_time - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
        deadline = start_time_zero + timedelta(del_day)
        deadline += timedelta(hours=18)
        deadline = deadline.strftime("%Y-%m-%d %H:%M")
    elif int(cycle_id) == 4:
        # 每月任务
        current_year = start_time.year
        current_month = start_time.month
        # 获取当前月第一天的星期和当月的总天数
        firstDayWeekDay, monthRange = calendar.monthrange(current_year, current_month)
        # 获取当前月的 最后一天
        lastDay = datetime.datetime(year=current_year, month=current_month, day=monthRange)
        deadline += timedelta(hours=18)
        deadline = lastDay.strftime("%Y-%m-%d %H:%M:%S")
    return start_time,deadline


def calculate_expire_date(weekday):
    """计算等待审核过期时间"""
    if weekday < 3:
        del_day = 2
    elif weekday in [3, 4, 5]:
        del_day = 4
    elif weekday == 6:
        del_day = 3
    return del_day

