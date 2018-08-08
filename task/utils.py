import json
import datetime
import calendar


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


def build_attachment_info(id_dict, attachment):
    att_list = []
    attachment = json.loads(attachment)
    for item in list(attachment):
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


def compare_json(record, modify_info, id_key):
    # json 数据对比
    id_key = str(id_key)
    insert_list = []
    update_list = []
    update_id_list = []
    delete_list_id_list = []
    for item in modify_info:
        id = item.get(id_key,None)
        if id:
             update_id_list.append(int(id))
             update_list.append(item)
        else:
            insert_list.append(item)
    for item in record:
        key = getattr(item, id_key)
        if int(key) not in update_id_list:
            delete_list_id_list.append(item.pk)
    return insert_list, update_list, delete_list_id_list


def build_statistic_filter(dpid,sid,first_day,last_day):
    filter={}
    filter['first_day'],filter["last_day"]=first_day,last_day
    if int(sid) != 0:
        filter["sid"] = sid
    elif int(dpid) != 0:
        filter["dpid"] = dpid
    return filter


def getMonthFirstDayAndLastDay(year_month):
    """
    :param year: 年份，默认是本年，可传int或str类型
    :param month: 月份，默认是本月，可传int或str类型
    :return: firstDay: 当月的第一天，datetime.date类型
              lastDay: 当月的最后一天，datetime.date类型
    """
    year, month = str(year_month).split("-")
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year

    if month:
        month = int(month)
    else:
        month = datetime.date.today().month

    # 获取当月第一天的星期和当月的总天数
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)
    # 获取当月的第一天
    firstDay = datetime.date(year=year, month=month, day=1)
    lastDay = datetime.date(year=year, month=month, day=monthRange)

    print(firstDay,lastDay)

    return firstDay, lastDay
