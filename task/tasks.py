# Create your tasks here
from django.db import transaction
import datetime
from .server import *
from thinking_library.celery import app
from common.functions import filter_fields
from .utils import calculate_deadline


@app.task
def daily_task():
    """指派日常任务"""
    print("日常任务")
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
                    task_assign_db.mutil_insert_task_assign(assigner_list)
        except Exception as e:
            print(e)

@app.task
def weekly_task():
    """指派周期任务"""
    print("指派周期任务")
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
                    task_assign_db.mutil_insert_task_assign(assigner_list)
        except Exception as e:
            print(e)


@app.task
def monthly_task():
    """指派月任务"""
    print("月任务")
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
                    task_assign_db.mutil_insert_task_assign(assigner_list)
        except Exception as e:
            print(e)


