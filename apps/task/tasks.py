# Create your tasks here
from thinking_library.settings import res
from django.db import transaction
import datetime
from .server import *
from thinking_library.celery import app
from common.functions import filter_fields
from .utils import calculate_deadline,calculate_expire_date
from notice.views import notice_add


@app.task
def daily_task():
    """指派日常任务"""
    cycle = 2
    today = datetime.datetime.today()
    # 获取周期任务
    task_list = task_period_db.query_expire_task(cycle, today)
    if task_list:
        try:
            with transaction.atomic():
                for task_obj in task_list:
                    # 转化为字典
                    task_dict = task_obj.__dict__
                    tpid = task_dict["tpid"]
                    # 参数过滤
                    start_time, deadline = calculate_deadline(task_dict["cycle_id"], task_dict["deadline"])
                    modify_info = filter_fields(TaskMap._insert, task_dict)
                    modify_info["start_time"] = start_time
                    modify_info["deadline"] = deadline
                    tmid = task_map_db.insert_task(modify_info)
                    # 插入标签
                    task_tag_list = task_period_tag_db.query_tag_by_tpid(tpid)
                    tag_list = []
                    for obj in task_tag_list:
                        tag_json = {}
                        tag_json["tmid_id"] = tmid
                        tag_json["name"] = obj.name
                        tag_list.append(tag_json)
                    if tag_list:
                        task_map_tag_db.mutil_insert_tag(tag_list)
                    # 插入指派附件
                    task_att_list = task_period_att_db.query_attachment_by_tpid(tpid)
                    att_list = []
                    for obj in task_att_list:
                        att_json = {}
                        att_json["tmid_id"] = tmid
                        att_json["attachment"] = obj.attachment
                        att_json["description"] = obj.description
                        att_json["name"] = obj.name
                        att_list.append(att_json)
                    if att_list:
                        task_map_att_db.mutil_insert_attachment(att_list)
                    # 插入审核人
                    reviewers = task_period_review_db.query_task_reviewer_by_tpid(tpid)
                    reviewers_list = []
                    for item in reviewers:
                        att_json = {}
                        att_json['tmid_id'] = tmid
                        att_json["sid_id"] = item.sid_id
                        att_json["follow"] = item.follow
                        reviewers_list.append(att_json)
                    task_review_db.mutil_insert_reviewer(reviewers_list)
                    # 插入指派对象
                    assigners = task_period_assigner_db.query_task_assigner_by_tpid(tpid)
                    assigner_list = []
                    for item in assigners:
                        # 查看任务周期类型，根据任务周期计算截止时间
                        ass_json = {}
                        ass_json['tmid_id'] = tmid
                        ass_json["member_id_id"] = item.member_id_id
                        ass_json["start_time"] = start_time
                        ass_json["deadline"] = deadline
                        assigner_list.append(ass_json)
                        # 指派任务
                    for obj in assigner_list:
                            tasid = task_assign_db.insert_task_assign(obj)
                            # 插入任务审核结果记录信息
                            review_result = []
                            for item in reviewers:
                                result_dict = {}
                                result_dict["tasid_id"] = tasid
                                result_dict["sid_id"] = item.sid_id
                                result_dict["follow"] = item["follow"]
                                result_dict["result"] = 0
                                review_result.append(result_dict)
                            task_review_result_db.mutil_insert(review_result)
                    # 指派通知
                    data_manage = {
                        'notice_title': '您有一个新的工单！',
                        'notice_body': modify_info.get("title"),
                        'notice_url': '/task/personal',
                        'notice_type': 'notice',
                    }
                    for item in assigner_list:
                        notice_add(item.get("member_id_id", 0), data_manage)
        except Exception as e:
            print(e)

@app.task
def weekly_task():
    """指派周期任务"""
    cycle = 3
    today = datetime.datetime.today()
    # 获取周期任务
    task_list = task_period_db.query_expire_task(cycle, today)
    if task_list:
        try:
            with transaction.atomic():
                for task_obj in task_list:
                    # 转化为字典
                    task_dict = task_obj.__dict__
                    tpid = task_dict["tpid"]
                    # 参数过滤
                    start_time, deadline = calculate_deadline(task_dict["cycle_id"], task_dict["deadline"])
                    modify_info = filter_fields(TaskMap._insert, task_dict)
                    modify_info["start_time"] = start_time
                    modify_info["deadline"] = deadline
                    tmid = task_map_db.insert_task(modify_info)
                    # 插入标签
                    task_tag_list = task_period_tag_db.query_tag_by_tpid(tpid)
                    tag_list = []
                    for obj in task_tag_list:
                        tag_json = {}
                        tag_json["tmid_id"] = tmid
                        tag_json["name"] = obj.name
                        tag_list.append(tag_json)
                    if tag_list:
                        task_map_tag_db.mutil_insert_tag(tag_list)
                    # 插入指派附件
                    task_att_list = task_period_att_db.query_attachment_by_tpid(tpid)
                    att_list = []
                    for obj in task_att_list:
                        att_json = {}
                        att_json["tmid_id"] = tmid
                        att_json["attachment"] = obj.attachment
                        att_json["description"] = obj.description
                        att_json["name"] = obj.name
                        att_list.append(att_json)
                    if att_list:
                        task_map_att_db.mutil_insert_attachment(att_list)
                    # 插入审核人
                    reviewers = task_period_review_db.query_task_reviewer_by_tpid(tpid)
                    reviewers_list = []
                    for item in reviewers:
                        att_json = {}
                        att_json['tmid_id'] = tmid
                        att_json["sid_id"] = item.sid_id
                        att_json["follow"] = item.follow
                        reviewers_list.append(att_json)
                    task_review_db.mutil_insert_reviewer(reviewers_list)
                    # 插入指派对象
                    assigners = task_period_assigner_db.query_task_assigner_by_tpid(tpid)
                    assigner_list = []
                    for item in assigners:
                        # 查看任务周期类型，根据任务周期计算截止时间
                        ass_json = {}
                        ass_json['tmid_id'] = tmid
                        ass_json["member_id_id"] = item.member_id_id
                        ass_json["start_time"] = start_time
                        ass_json["deadline"] = deadline
                        assigner_list.append(ass_json)
                    # task_assign_db.mutil_insert_task_assign(assigner_list)
                    # 指派任务
                    for obj in assigner_list:
                        tasid = task_assign_db.insert_task_assign(obj)
                        # 插入任务审核结果记录信息
                        review_result = []
                        for item in reviewers:
                            result_dict = {}
                            result_dict["tasid_id"] = tasid
                            result_dict["sid_id"] = item.sid_id
                            result_dict["follow"] = item["follow"]
                            result_dict["result"] = 0
                            review_result.append(result_dict)
                        task_review_result_db.mutil_insert(review_result)
                    # 指派通知
                    data_manage = {
                        'notice_title': '您有一个新的工单！',
                        'notice_body': modify_info.get("title"),
                        'notice_url': '/task/personal',
                        'notice_type': 'notice',
                    }
                    for item in assigner_list:
                        notice_add(item.get("member_id_id", 0), data_manage)
        except Exception as e:
            print(e)


@app.task
def monthly_task():
    """指派月任务"""
    cycle = 4
    today = datetime.datetime.today()
    # 获取周期任务
    task_list = task_period_db.query_expire_task(cycle, today)
    if task_list:
        try:
            with transaction.atomic():
                for task_obj in task_list:
                    # 转化为字典
                    task_dict = task_obj.__dict__
                    tpid = task_dict["tpid"]
                    # 参数过滤
                    start_time, deadline = calculate_deadline(task_dict["cycle_id"], task_dict["deadline"])
                    modify_info = filter_fields(TaskMap._insert, task_dict)
                    modify_info["start_time"] = start_time
                    modify_info["deadline"] = deadline
                    tmid = task_map_db.insert_task(modify_info)
                    # 插入标签
                    task_tag_list = task_period_tag_db.query_tag_by_tpid(tpid)
                    tag_list = []
                    for obj in task_tag_list:
                        tag_json = {}
                        tag_json["tmid_id"] = tmid
                        tag_json["name"] = obj.name
                        tag_list.append(tag_json)
                    if tag_list:
                        task_map_tag_db.mutil_insert_tag(tag_list)
                    # 插入指派附件
                    task_att_list = task_period_att_db.query_attachment_by_tpid(tpid)
                    att_list = []
                    for obj in task_att_list:
                        att_json = {}
                        att_json["tmid_id"] = tmid
                        att_json["attachment"] = obj.attachment
                        att_json["description"] = obj.description
                        att_json["name"] = obj.name
                        att_list.append(att_json)
                    if att_list:
                        task_map_att_db.mutil_insert_attachment(att_list)
                    # 插入审核人
                    reviewers = task_period_review_db.query_task_reviewer_by_tpid(tpid)
                    reviewers_list = []
                    for item in reviewers:
                        att_json = {}
                        att_json['tmid_id'] = tmid
                        att_json["sid_id"] = item.sid_id
                        att_json["follow"] = item.follow
                        reviewers_list.append(att_json)
                    task_review_db.mutil_insert_reviewer(reviewers_list)
                    # 插入指派对象
                    assigners = task_period_assigner_db.query_task_assigner_by_tpid(tpid)
                    assigner_list = []
                    for item in assigners:
                        # 查看任务周期类型，根据任务周期计算截止时间
                        ass_json = {}
                        ass_json['tmid_id'] = tmid
                        ass_json["member_id_id"] = item.member_id_id
                        ass_json["start_time"] = start_time
                        ass_json["deadline"] = deadline
                        assigner_list.append(ass_json)
                    # task_assign_db.mutil_insert_task_assign(assigner_list)
                    # 指派任务
                    for obj in assigner_list:
                        tasid = task_assign_db.insert_task_assign(obj)
                        # 插入任务审核结果记录信息
                        review_result = []
                        for item in reviewers:
                            result_dict = {}
                            result_dict["tasid_id"] = tasid
                            result_dict["sid_id"] = item.sid_id
                            result_dict["follow"] = item["follow"]
                            result_dict["result"] = 0
                            review_result.append(result_dict)
                        task_review_result_db.mutil_insert(review_result)
                    # 指派通知
                    data_manage = {
                        'notice_title': '您有一个新的工单！',
                        'notice_body': modify_info.get("title"),
                        'notice_url': '/task/personal',
                        'notice_type': 'notice',
                    }
                    for item in assigner_list:
                        notice_add(item.get("member_id_id", 0), data_manage)
        except Exception as e:
            print(e)


@app.task
def task_auot_review():
    """自动审核到期任务"""
    # 获取所有等待审核人任务
    k1="task_review"
    task_tuple = res.hgetall(k1),
    for item in task_tuple:
        for k in item:
            key = str(k,encoding="utf-8")
            value = str(item[k],encoding="utf-8")
            now_time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            # 已过期，审核自动通过
            modify = {"result": 3}
            if now_time > value:
                # 查看是否为次序审核任务，且未审核
                query_set=task_review_result_db.query_task_review_by_follow(key)
                if query_set:
                    # 次序审核,通过
                    query_set.update(**modify)
                    # 更新过期时间
                    weekday = datetime.datetime.today().weekday()
                    del_day = calculate_expire_date(weekday)
                    expire_date = now_time+timedelta(del_day)
                    res.hset(k1, key, expire_date)
                    # 最后一条则删除缓存
                    if len(query_set) == 1:
                        res.hdel(k1,key)
                else:
                    # 自动审核通过
                    task_review_result_db.auto_update_result(key,modify)
                    # 删除过期审核
                    res.hdel(k1, key)


