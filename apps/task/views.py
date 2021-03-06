import copy
import json
import os
import uuid
import datetime
from  thinking_library.settings import res
from django.core import serializers
from django.db import transaction
from django.http import StreamingHttpResponse
from django.shortcuts import render, HttpResponse,redirect
from django.core.cache import cache
from task.forms.form import *
from common.functions import *
from personnel.server import staff_db,department_db
from .server import *
from .utils import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required,permission_required
# Create your views here.
from django.conf import settings
from .tasks import weekly_task,task_auot_review
from notice.views import notice_add


def index(request):

    # print(request.session[settings.PERMISSION_URL_DICT_KEY])
    weekly_task()
    task_auot_review()
    cache.set("user_id",123)

    staff = request.user.staff
    return render(request,'layout.html')


def home(request):
    return render(request,'index_v3.html')


def task_edit(request):
    """任务编辑"""
    method = request.method
    if method == "GET":
        tid = request.GET.get("tid", None)
        if tid:
            # 编辑
            # 获取任务信息及其标签信息、附件信息、审核人
            task_info = task_db.query_task_by_tid(tid)
            task_tag_info = task_tag_db.query_task_tag_by_tid(tid)
            task_attachment_info = task_attachment_db.query_task_attachment_by_tid(tid)
        else:
            # 创建
            tid = 0
            task_info = {}
            task_tag_info = {}
            task_attachment_info = {}
        return render(request, 'task/task_edit.html',{"tid": tid,
                                                      "task_info": task_info,
                                                      "task_tag_info": task_tag_info,
                                                      "task_attachment_data": task_attachment_info,
                                                      })
    else:
        ret = {"status": False, "data": "", "message": ""}
        form = TaskForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            # 获取任务id
            tid = data.get("tid", None)
            # 获取附件并删除
            attachment = data.get("attachment", None)
            data.pop("attachment")
            attachment_list = list(json.loads(attachment))
            if tid:
                # 编辑
                # 获取标签并删除
                tags = data.get("tags", None)
                data.pop("tags")
                tag_list = list(json.loads(tags))
                try:
                    with transaction.atomic():
                        # 更新任务
                        task_db.update_task(data)
                        # 更新标签
                        tags_record = task_tag_db.query_task_tag_by_tid(tid)
                        # 数据对比
                        insert_tag, update_tag, delete_tag_id = compare_json(tags_record, tag_list, "ttid")
                        if insert_tag:
                            task_tag_db.mutil_insert_tag(insert_tag)
                        if update_tag:
                            task_tag_db.mutil_update_tag(update_tag)
                        if delete_tag_id:
                            task_tag_db.mutil_delete_tag(delete_tag_id)
                        # 更新附件
                        att_record = task_attachment_db.query_task_attachment_by_tid(tid)
                        # 数据对比
                        insert_att, update_att, delete_id_att = compare_json(att_record, attachment_list, "tamid")
                        if insert_att:
                            task_attachment_db.mutil_insert_attachment(insert_att)
                        if update_att:
                            task_attachment_db.mutil_update_attachment(update_att)
                        if delete_id_att:
                            task_attachment_db.mutil_delete_task_attachment(delete_id_att)
                        ret['status'] = True
                        ret["data"] = tid
                except Exception as e:
                    ret["message"] = "更新失败"
            else:
                # 创建
                # 获取标签并删除
                tags = data.get("tags", None)
                tag_list = tags.split("|")
                data.pop("tags")
                try:
                    with transaction.atomic():
                        tid = task_db.insert_task(data)
                        # 如果任务插入成功
                        if tid:
                            # 插入标签
                            id_dict = {"tid_id": tid}
                            tags_list = build_tags_info(id_dict, tag_list)
                            task_tag_db.mutil_insert_tag(tags_list)
                            # 插入附件
                            attachment_list = build_attachment_info(id_dict, attachment_list)
                            task_attachment_db.mutil_insert_attachment(attachment_list)
                        ret["status"] = True
                        ret['data'] = tid
                except Exception as e:
                    print(e)
                    ret["message"] = "创建失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def task_map_content(request):
    """任务指派内容编辑"""
    method = request.method
    if method == "GET":
        tmid = request.GET.get("tmid", None)
        if tmid:
            # 编辑
            # 获取任务信息及其标签信息、附件信息
            task_map_info = task_map_db.query_task_by_tmid(tmid)
            task_map_tag_info = task_map_tag_db.query_tag_by_tmid(tmid)
            task_map_attach_info = task_map_att_db.query_attachment_by_tmid(tmid)
        else:
            # 创建
            tmid = 0
            task_map_info = {}
            task_map_tag_info = {}
            task_map_attach_info = {}
        return render(request, 'task/task_map_edit.html',{"tmid": tmid,
                                                      "task_info": task_map_info,
                                                      "task_tag_info": task_map_tag_info,
                                                      "task_attachment_data": task_map_attach_info,})
    else:
        ret = {"status": False, "data": "", "message": ""}
        form = TaskForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            # 获取任务id
            tmid = data.get("tmid", None)
            # 获取附件并删除
            attachment = data.get("attachment", None)
            data.pop("attachment")
            attachment_list = list(json.loads(attachment))
            if tmid:
                # 编辑
                # 获取标签并删除
                tags = data.get("tags", None)
                data.pop("tags")
                tag_list = list(json.loads(tags))
                try:
                    with transaction.atomic():
                        # 更新任务
                        task_map_db.update_task(data)
                        # 更新标签
                        tags_record = task_map_tag_db.query_tag_by_tmid(tmid)
                        # 数据对比
                        insert_tag, update_tag, delete_tag_id = compare_json(tags_record, tag_list, "tmtid")
                        if insert_tag:
                            task_map_tag_db.mutil_insert_tag(insert_tag)
                        if update_tag:
                            task_map_tag_db.mutil_update_tag(update_tag)
                        if delete_tag_id:
                            task_map_tag_db.mutil_delete_tag(delete_tag_id)
                        # 更新附件
                        att_record = task_map_att_db.query_attachment_by_tmid(tmid)
                        # 数据对比
                        insert_att, update_att, delete_id_att = compare_json(att_record, attachment_list, "tmaid")
                        if insert_att:
                            task_map_att_db.mutil_insert_attachment(insert_att)
                        if update_att:
                            task_map_att_db.mutil_update_attachment(update_att)
                        if delete_id_att:
                            task_map_att_db.mutil_delete_attachment(delete_id_att)
                        ret['status'] = True
                        ret["data"] = tmid
                except Exception as e:
                    print(e)
                    ret["message"] = "更新失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def task_detail(request):
    """查看任务详细"""
    tmid = request.GET.get("tmid", None)
    task_obj = task_map_db.query_task_by_tmid(tmid)
    return render(request, 'task/task_detail.html', {"task_obj": task_obj})


def task_period_detail(request):
    """查看任务周期详细"""
    tpid = request.GET.get("tpid", None)
    task_obj = task_period_db.query_task_by_tpid(tpid)
    return render(request, 'task/task_period_detail.html', {"task_obj": task_obj})


def task_base_detail(request):
    """查看待指派任务详细"""
    tid = request.GET.get("tid", None)
    # 据任务分配ID获取内容
    task_obj = task_db.query_task_by_tid(tid)
    if task_obj:
        return render(request, 'task/task_base_detail.html', {"task_obj": task_obj})
    return render(request, '404.html')


# def task_delete(request):
#     """任务删除"""
#     ret = {'status': '', "data": "","message": ""}
#     ids = request.GET.get("ids", '')
#     ids = ids.split("|")
#     # 转化成数字
#     id_list = []
#     for item in ids:
#         if item:
#             id_list.append(int(item))
#     try:
#         with transaction.atomic():
#             # 删除任务
#             task_db.multi_delete_task(id_list)
#             # 删除附件
#             task_attachment_db.multi_delete_attach_by_tid(id_list)
#             # 删除标签
#             task_tag_db.mutil_delete_tag_by_tid(id_list)
#             # 删除审核人
#             task_review_db.mutil_delete_reviewer_by_tid(id_list)
#             # # 删除任务指派
#             # for item in id_list:
#             #     # 获取任务指派id
#             #     assign_objs=task_assign_db.query_task_assign_by_tid(item)
#             # task_assign_db.mutil_delete_reviewer_by_tid(id_list)
#             # # 删除任务指派附件
#             ret['status'] = True
#     except Exception as e:
#         ret["message"] = "删除失败"
#     return HttpResponse(json.dumps(ret))


def task_delete(request):
    """任务软删除"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    status = {"delete_status": 0}
    try:
        task_db.multi_delete_task(id_list, status)
        ret['status'] = True
    except Exception as e:
        print(e)
        ret['status'] = "删除失败"
    return HttpResponse(json.dumps(ret))


def task_map_delete(request):
    """指派任务软删除"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    status = {"status": 0} # 更改为删除状态
    try:
        task_map_db.multi_delete(id_list, status)
        # 查看任务是否已经完成
        for id in id_list:
            task_map_obj = task_map_db.query_task_by_tmid(id)
            # 未完成则与其相关的指派任务该为取消状态
            if not task_map_obj.is_finish:
                status = {"status", 0}
                task_assign_db.update_status_by_tmid(id, status)
        ret['status'] = True
    except Exception as e:
        print(e)
        ret['status'] = "删除失败"
    return HttpResponse(json.dumps(ret))


def task_period_delete(request):
    """周期任务软删除"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    status = {"status": 0} # 更改为删除状态
    try:
        task_period_db.multi_delete(id_list, status)
        # 查看任务是否已经完成
        ret['status'] = True
    except Exception as e:
        ret['status'] = "删除失败"
    return HttpResponse(json.dumps(ret))


def task_map_cancel(request):
    """指派任务取消"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    status = {"status": 3}  # 更改为取消状态
    try:
        task_map_db.multi_delete(id_list, status)
        # 查看任务是否已经完成
        for id in id_list:
            task_map_obj = task_map_db.query_task_by_tmid(id)
            # 未完成则与其相关的指派任务该为取消状态
            if not task_map_obj.is_finish:
                status = {"status": 0,"is_finish":3}
                task_assign_db.update_status_by_tmid(id, status)
        ret['status'] = True
    except Exception as e:
        ret['status'] = "任务取消失败，已完成任务无法取消"
    return HttpResponse(json.dumps(ret))


def task_period_cancel(request):
    """取消周期任务"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    status = {"status": 3}  # 更改为取消状态
    try:
        task_period_db.multi_delete(id_list, status)
        # 查看任务是否已经完成
        ret['status'] = True
    except Exception as e:
        ret['status'] = "周期任务取消失败"
    return HttpResponse(json.dumps(ret))


# def task_mutil_assign(request):
#     """批量任务指派"""
#     ret = {"status": False, "data": '', "message": ''}
#     assign = request.POST.get("task_assign", None)
#     task_assign_list = list(json.loads(assign))
#     if task_assign_list:
#         try:
#             with transaction.atomic():
#                 task_assign_db.mutil_insert_task_assign(task_assign_list)
#                 # 将任务状态更改为已指派
#                 modify_info = {"is_assign": 1}
#                 for item in task_assign_list:
#                     task_db.update_task_status_by_tid(item['tid_id'], modify_info)
#                 ret['status'] = True
#         except Exception as e:
#             ret['message'] = str(e)
#     else:
#         ret['message'] = "至少选择一个员工"
#     return HttpResponse(json.dumps(ret))


# def task_team_assign(request):
#     """组队任务指派"""
#     ret = {"status": False, "data": '', "message": ''}
#     assign = request.POST.get("team_assign", None)
#     task_assign_list = list(json.loads(assign))
#     if task_assign_list:
#         tid = task_assign_list[0]['tid']
#         try:
#             with transaction.atomic():
#                 task_assign_db.mutil_insert_task_assign(task_assign_list)
#                 # 将任务状态更改为已指派,任务方式更改为组队任务
#                 modify_info = {"is_assign": 1, 'team':1}
#                 task_db.update_task_status_by_tid(tid, modify_info)
#                 ret['status'] = True
#         except Exception as e:
#             ret['message'] = str(e)
#     else:
#         ret['message'] = "至少选择一个员工"
#     return HttpResponse(json.dumps(ret))


def task_assign(request):
    """任务指派"""
    method = request.method
    if method == "GET":
        team = request.GET.get('team', None)
        tids = request.GET.get("tids",None)
        if tids:
            edit = 0  # 0 表示指派，1表示编辑
            tid_list = tids.split("|")
            # 转化成数字
            id_list = []
            for item in tid_list:
                if item:
                    id_list.append(int(item))
            query_sets = task_db.query_task_by_tids(id_list)
            return render(request,'task/task_assign.html',{"query_sets":query_sets,"team":team,"tids":tids,"edit":edit})
        return render(request,'404.html')
    else:
        ret = {"status": False, "data": "", "message": ''}
        data = request.POST
        form = TaskMapForm(data=data)
        if form.is_valid():
            # 获取任务id并删除
            data = data.dict()
            tids = data.get("tids", None)
            data.pop("tids")
            tids_list = tids.split("|")
            # 获取指派人并删除
            assigners = data.get("assigners", None)
            assigners = list(json.loads(assigners))
            data.pop("assigners")
            # 获取审核人并删除
            reviewers = data.get("reviewers", None)
            reviewers = list(json.loads(reviewers))
            data.pop("reviewers")
            # 插入指派任务
            task_list = []
            for tid in tids_list:
                item = data.copy()
                # 获取任务内容
                task_obj = task_db.query_task_by_tid(int(tid))
                if task_obj:
                    item["tid_id"] = task_obj.tid
                    item["title"] = task_obj.title
                    item["content"] = task_obj.content
                    item['type_id'] = task_obj.type_id
                task_list.append(item)
            try:
                with transaction.atomic():
                    for modify in task_list:
                        # 查看是否为周期还是单次任务
                        if int(modify["cycle_id"]) > 1:
                            # 周期任务,把信息保存到周期任务相关表中
                            tpid = task_period_db.insert_task(modify)
                            tid = modify["tid_id"]
                            # 插入指派附件
                            # 获取附件内容
                            task_att_list = task_attachment_db.query_task_attachment_by_tid(tid)
                            att_list = []
                            for obj in task_att_list:
                                att_json = {}
                                att_json["tpid_id"] = tpid
                                att_json["attachment"] = obj.attachment
                                att_json["description"] = obj.description
                                att_json["name"] = obj.name
                                att_list.append(att_json)
                            if att_list:
                                task_period_att_db.mutil_insert_attachment(att_list)
                            # 插入指派标签
                            task_tag_list = task_tag_db.query_task_tag_by_tid(tid)
                            tag_list = []
                            for obj in task_tag_list:
                                tag_json = {}
                                tag_json["tpid_id"] = tpid
                                tag_json["name"] = obj.name
                                tag_list.append(tag_json)
                            if tag_list:
                                task_period_tag_db.mutil_insert_tag(tag_list)
                            # 插入指派对象
                            period_assigner_list = []
                            period_assigner = copy.deepcopy(assigners)
                            for item in period_assigner:
                                item['tpid_id'] = tpid
                                period_assigner_list.append(item)
                            task_period_assigner_db.mutil_insert_assigner(period_assigner_list)
                            # 插入审核人
                            reviewers_list = []
                            period_reviewers = copy.deepcopy(reviewers)
                            for item in period_reviewers:
                                item['tpid_id'] = tpid
                                reviewers_list.append(item)
                            task_period_review_db.mutil_insert_reviewer(reviewers_list)
                        tmid = task_map_db.insert_task(modify)
                        tid = modify["tid_id"]
                        # 插入指派附件
                        task_att_list = task_attachment_db.query_task_attachment_by_tid(tid)
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
                        # 插入指派标签
                        task_tag_list = task_tag_db.query_task_tag_by_tid(tid)
                        tag_list = []
                        for obj in task_tag_list:
                            tag_json = {}
                            tag_json["tmid_id"] = tmid
                            tag_json["name"] = obj.name
                            tag_list.append(tag_json)
                        if tag_list:
                            task_map_tag_db.mutil_insert_tag(tag_list)
                        # 插入指派对象
                        assigner_list = []
                        for item in assigners:
                            # 查看任务周期类型，根据任务周期计算截止时间
                            start_time,deadline = calculate_deadline(data["cycle_id"],data["deadline"],data["start_time"])
                            item['tmid_id'] = tmid
                            item["start_time"] = start_time
                            item["deadline"] = deadline
                            assigner_list.append(item)
                        # task_assign_db.mutil_insert_task_assign(assigner_list)
                        for obj in assigner_list:
                            tasid = task_assign_db.insert_task_assign(obj)
                            # 插入任务审核结果记录信息
                            review_result = []
                            for item in reviewers:
                                result_dict ={}
                                result_dict["tasid_id"] = tasid
                                result_dict["sid_id"] = item['sid_id']
                                result_dict["follow"] = item["follow"]
                                result_dict["result"] = 0
                                review_result.append(result_dict)
                            task_review_result_db.mutil_insert(review_result)
                        # 指派通知
                        data_manage = {
                            'notice_title': '您有一个新的工单！',
                            'notice_body': modify.get("title"),
                            'notice_url': '/task/personal',
                            'notice_type': 'notice',
                        }
                        for item in assigner_list:
                            notice_add(item.get("member_id_id", 0), data_manage)
                        # 插入审核人
                        reviewers_list = []
                        for item in reviewers:
                            item['tmid_id'] = tmid
                            reviewers_list.append(item)
                        task_review_db.mutil_insert_reviewer(reviewers_list)
                    ret['status'] = True
                    ret['data'] = tmid
            except Exception as e:
                print(e)
                ret["message"] = "指派失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def task_map_edit(request):
    """编辑个人任务指派"""
    method = request.method
    if method == "GET":
        tmid = request.GET.get("tmid", None)
        edit = 1
        if tmid:
            query_sets = task_map_db.query_task_by_tmid(tmid)
            task_assign_info = task_assign_db.query_task_assign_by_tmid(tmid)
            task_review_info = task_review_db.query_task_reviewer_by_tmid(tmid)
            return render(request, 'task/task_assign.html', {"query_sets": query_sets, "edit":edit,
                                                             "task_assign_info": task_assign_info,
                                                             "task_review_info": task_review_info})
        return render(request,"404.html")
    else:
        ret = {"status": False, "data": "", "message": ''}
        data = request.POST
        form = TaskMapForm(data=data)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            # 获取任务指派id
            tmid = data.get("tmid", None)
            # 获取审核人并删除
            assigners = data.get("assigners", None)
            assigners_list = list(json.loads(assigners))
            data.pop("assigners")
            # 获取审核人并删除
            reviewers = data.get("reviewers", None)
            reviewers_list = list(json.loads(reviewers))
            data.pop("reviewers")
            if tmid:
                try:
                    with transaction.atomic():
                        # 更新任务
                        task_map_db.update_task(data)
                        # 更新审核人
                        reviewer_record = task_review_db.query_task_reviewer_by_tmid(tmid)
                        insert_review, update_review, delete_id_review = compare_json(reviewer_record, reviewers_list,
                                                                                      'tvid')
                        if insert_review:
                            task_review_db.mutil_insert_reviewer(insert_review)
                        if update_review:
                            task_review_db.mutil_update_reviewer(update_review)
                        if delete_id_review:
                            task_review_db.mutil_delete_reviewer(delete_id_review)
                        # 更新指派人
                        task_assign_record = task_assign_db.query_task_assign_by_tmid(tmid)
                        insert_assign, update_assign, delete_id_assign = compare_json(task_assign_record,
                                                                                      assigners_list,
                                                                                      'tasid')
                        if insert_assign:
                            task_assign_db.mutil_insert_task_assign(insert_assign)
                        if delete_id_assign:
                            # 删除任务指派
                            task_assign_db.mutil_delete_assign_by_tasid(delete_id_assign)
                            # 删除指派的任务标签附件
                            task_assign_tag_db.mutil_delete_tag_by_tasid(delete_id_assign)
                            task_assign_attach_db.mutil_delete_attach_by_tasid(delete_id_assign)
                    # 更新审核结果信息
                    task_assign = task_assign_db.query_task_assign_by_tmid(tmid)
                    review_result = []
                    for obj in task_assign:
                        review_list = task_review_db.query_task_reviewer_by_tmid(tmid)
                        for item in review_list:
                            result_dict={}
                            result_dict["tasid_id"]= obj.tasid
                            result_dict["sid_id"] = item.sid_id
                            result_dict["follow"] = item.follow
                            result_dict["result"] = 0
                            review_result.append(result_dict)
                    # 删除旧信息
                    for item in review_result:
                        task_review_result_db.delete_review_result(item["tasid_id"])
                    task_review_result_db.mutil_insert(review_result)
                    ret['status'] = True
                    ret["data"] = tmid
                except Exception as e:
                    print(e)
                    ret["message"] = "编辑失败"
            else:
                ret['message'] = "编辑失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def task_assign_list(request):
    """任务已指派列表"""
    method = request.method
    if method == "GET":
        filter = request.GET
        type_id = int(filter.get("s", 0))
        query_sets = task_map_db.query_task_lists()
        if type_id > 0:
            query_sets = query_sets.filter(type_id=type_id)
        return render(request, 'task/task_assigned_list.html', {"query_sets": query_sets})
    else:
        # 任务内容指派
        ret = {"status": "", "data": "", "message": ''}
        data = request.POST
        form = TaskAssignForm(data=data)
        if form.is_valid():
            data =request.POST
            data = data.dict()
            # 获取标签并删除
            tags = data.get("tags", None)
            tag_list = tags.split("|")
            data.pop("tags")
            # 获取附件并删除
            attachment = data.get("attachment", None)
            data.pop("attachment")
            if data:
                try:
                    with transaction.atomic():
                        tasid = data.get("tasid", None)
                        task_assign_db.update_task_assign(data)
                        # 插入标签
                        tags_assign_list = build_assign_tags_info(tasid, tag_list)
                        task_assign_tag_db.mutil_insert_assign_tag(tags_assign_list)
                        # 插入附件
                        attachment_list = build_assign_attach_info(tasid, attachment)
                        task_assign_attach_db.mutil_insert_assign_attach(attachment_list)
                        ret["status"] = True
                except Exception as e:
                    ret["message"] = "指派失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def task_period(request):
    """周期任务表"""
    method = request.method
    if method == "GET":
        filter = request.GET
        type_id = int(filter.get("s", 0))
        query_sets = task_period_db.query_task_lists()
        if type_id > 0:
            query_sets = query_sets.filter(type_id=type_id)
        return render(request, 'task/task_period_list.html', {"query_sets": query_sets})
    else:
        # 任务内容指派
        ret = {"status": "", "data": "", "message": ''}
        data = request.POST
        form = TaskAssignForm(data=data)
        if form.is_valid():
            data =request.POST
            data = data.dict()
            # 获取标签并删除
            tags = data.get("tags", None)
            tag_list = tags.split("|")
            data.pop("tags")
            # 获取附件并删除
            attachment = data.get("attachment", None)
            data.pop("attachment")
            if data:
                try:
                    with transaction.atomic():
                        tasid = data.get("tasid", None)
                        task_assign_db.update_task_assign(data)
                        # 插入标签
                        tags_assign_list = build_assign_tags_info(tasid, tag_list)
                        task_assign_tag_db.mutil_insert_assign_tag(tags_assign_list)
                        # 插入附件
                        attachment_list = build_assign_attach_info(tasid, attachment)
                        task_assign_attach_db.mutil_insert_assign_attach(attachment_list)
                        ret["status"] = True
                except Exception as e:
                    ret["message"] = "指派失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))

def task_assign_edit(request):
    """更新指派内容"""
    ret = {"status": "", "data": "", "message": ''}
    data = request.POST
    form = TaskAssignForm(data=data)
    tasid=data.get("tasid", None)
    if form.is_valid():
        data = request.POST
        data = data.dict()
        # 获取标签并删除
        tags = data.get("tags", None)
        tag_list = list(json.loads(tags))
        data.pop("tags")
        # 获取附件并删除
        attachment = data.get("attachment", None)
        attachment_list = list(json.loads(attachment))
        data.pop("attachment")
        if tasid:
            try:
                with transaction.atomic():
                    # 更新指派内容
                    task_assign_db.update_task_assign(data)
                    # 更新标签
                    tags_record = task_assign_tag_db.query_task_assign_tag_by_tasid(tasid)
                    # 数据对比
                    insert_tag, update_tag, delete_tag_id = compare_json(tags_record, tag_list, "tatid")
                    if insert_tag:
                        task_assign_tag_db.mutil_insert_assign_tag(insert_tag)
                    if update_tag:
                        task_assign_tag_db.mutil_update_assign_tag(update_tag)
                    if delete_tag_id:
                        task_assign_tag_db.mutil_delete_tag(delete_tag_id)
                    # 更新附件
                    att_record = task_assign_attach_db.query_task_assign_attach_by_tasid(tasid)
                    # 数据对比
                    insert_att, update_att, delete_id_att = compare_json(att_record, attachment_list, "taaid")
                    if insert_att:
                        task_assign_attach_db.mutil_insert_assign_attach(insert_att)
                    if update_att:
                        task_assign_attach_db.mutil_update_assign_attach(update_att)
                    if delete_id_att:
                        task_assign_attach_db.mutil_delete_attach(delete_id_att)
                    ret['status'] = True
            except Exception as e:
                ret["message"] = str(e)
        else:
            ret['message'] = "找不到该对象信息"
    else:
        errors = form.errors.as_data().values()
        firsterror = str(list(errors)[0][0])
        ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def task_wait_review(request):
    """任务审核中心"""
    method = request.method
    if method == "GET":
        filter = request.GET
        type_id = int(filter.get("s", 0))
        # 获取所有已指派的任务
        # 待修改
        query_sets = task_map_db.query_task_lists()
        if type_id > 0:
            query_sets = query_sets.filter(type_id=type_id)
        return render(request, 'task/task_wait_review.html', {"query_sets": query_sets,"filter":type_id})


def personal_task_review(request):
    """我的审核任务"""
    method = request.method
    user_id = request.user.staff.sid
    if method == "GET":
        filter = request.GET
        type_id = int(filter.get("s", 0))
        # 根据用户id去获取审核任务
        task_review = task_review_db.query_task_reviewer_by_sid(user_id)
        tmid_list = []
        for item in task_review:
            tmid_list.append(item.tmid_id)
        # 获取相应的任务
        query_sets = task_map_db.query_task_by_tids(tmid_list)
        if type_id > 0:
            query_sets = query_sets.filter(type_id=type_id)
        return render(request, 'task/personal_task_review.html', {"query_sets": query_sets,"filter":type_id})


def task_review(request):
    """任务审核"""
    method = request.method
    if method == "GET":
        user_id = request.user.staff.sid
        tasid = request.GET.get("tasid", None)
        if tasid:
            tasid = int(tasid)
            # 获取任务指派内容
            task_assign_info = task_assign_db.query_task_assign_by_tasid(tasid)
            task_assign_info = task_assign_info.first()
            if task_assign_info:
                # 获取员工信息
                member_info = staff_db.query_staff_by_id(task_assign_info.member_id_id)
                # 获取任务提交记录
                task_submit_record = task_submit_record_db.query_submit_by_tasid(tasid)
                # 获取我的审核任务id
                task_review = task_review_db.query_task_reviewer_by_tid_sid(task_assign_info.tmid_id, user_id)
                # 获取我的审核记录
                task_review_record = task_review_record_db.query_task_review_record_list_by_tvid_and_tasid(task_review.tvid,tasid)
                return render(request, 'task/task_review.html', {
                                                                 "member_info": member_info,
                                                                 "task_review": task_review,
                                                                 'task_assign_info': task_assign_info,
                                                                 "task_submit_record": task_submit_record,
                                                                 "task_review_record": task_review_record})
        return render(request,"404.html")

    else:
        user_id = request.user.staff.sid
        ret = {'status': False, 'message':'', 'data':''}
        data = request.POST
        tasid = data['tasid_id']
        form = TaskReviewForm(data=data)
        if form.is_valid():
            try:
                with transaction.atomic():
                    data = data.dict()
                    task_review_record_db.insert_review_record(data)
                    is_complete = int(data["is_complete"])
                    # 如果通过 更新相应任务的完成状态
                    is_finish = True
                    is_reviewed = True
                    task_assign_obj = task_assign_db.query_task_assign_by_tasid(tasid).first()
                    if is_complete > 0:
                        # 更新该任务审核状态
                        result = {"result": 2}
                        task_review_result_db.update_result(tasid,user_id,result)
                        # 审核通过通知
                        data_manage = {
                            'notice_title': '工单审核通过！',
                            'notice_body': data["comment"],
                            'notice_url': '/task/personal',
                            'notice_type': 'notice',
                        }
                        notice_add(task_assign_obj.member_id_id, data_manage)
                        # check 是否所有审核人都确认通过
                        review_result = task_review_result_db.query_task_review_by_tasid(tasid)
                        for item in review_result:
                            if item.result < 2:
                                is_finish = False
                            # 检查是否所有人都已审核过，则清除缓存自动审核任务
                            if item.result == 0:
                                is_reviewed = False
                        if is_reviewed:
                            k1 = "task_review"
                            res.hdel(k1, tasid)
                        # check 是否所有审核人都确认通过
                        # 获取任务id
                        # task_assign_obj = task_assign_db.query_task_assign_by_tasid(tasid)
                        # task_assign_obj = task_assign_obj.first()
                        # tmid = task_assign_obj.tmid_id
                        # 获取任务审核人
                        # task_review_list = task_review_db.query_task_reviewer_by_tmid(task_assign_obj.tmid_id)
                        # 遍历该所有审核人对其的记录
                        # for item in task_review_list:
                        #     last_review_record = task_review_record_db.query_task_review_record_last_by_tvid_and_tasid(item.tvid,tasid)
                        #     if not last_review_record:
                        #         is_finish = False
                        #         break
                        #     else:
                        #         if not last_review_record.is_complete:
                        #             is_finish = False
                        #             break
                        if is_finish:
                            # 更新任务为通过状态
                            query_sets = task_assign_db.query_task_assign_by_tasid(tasid)
                            query_sets.update(is_finish=1)
                            # 添加任务绩效
                            task_assign_obj = task_assign_db.query_task_assign_by_tasid(tasid)
                            task_assign_obj = task_assign_obj.first()
                            tmid = task_assign_obj.tmid_id
                            task_map_obj = task_map_db.query_task_by_tmid(tmid)
                            performence_obj = performence_db.query_performence_by_pid(task_map_obj.perfor_id)
                            score = performence_obj.personal_score
                            perf_data = {"tmid_id": tmid, "sid_id": user_id, "personal_score": score}
                            performance_record_db.insert_performence_record(perf_data)
                            # 检查任务是否是团队任务
                            if task_map_obj.team == 1:
                                # 检查任务是否全部完成后
                                task_assign_list = task_assign_db.query_task_assign_by_tmid(tmid)
                                checked = True
                                for obj in task_assign_list:
                                    if obj.is_finish == 0:
                                        checked = False
                                        break
                                if checked:
                                    # 添加团队绩效
                                    for item in task_assign_list:
                                        performance_obj ={"sid_id":item.sid_id,"tmid_id":item.tmid_id,"team_score": performence_obj.team_score}
                                        performance_record_db.update_performence_record(performance_obj)
                    else:
                        # 更新该任务审核状态
                        result = {"result": 1}
                        task_review_result_db.update_result(tasid, user_id, result)
                        # 审核驳回通知
                        data_manage = {
                            'notice_title': '工单被驳回！',
                            'notice_body': data["reason"],
                            'notice_url': '/task/personal',
                            'notice_type': 'notice',
                        }
                        notice_add(task_assign_obj.member_id_id, data_manage)
                    ret['status'] = True
            except Exception as e:
                print(e)
                ret["message"] = "任务审核提交失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def task_review_record(request):
    """任务审核记录"""
    method = request.method
    if method == "GET":
        tasid = request.GET.get("tasid", None)
        if tasid:
            tasid = int(tasid)
            # 获取任务指派内容
            task_assign_info = task_assign_db.query_task_assign_by_tasid(tasid)
            task_assign_info = task_assign_info.first()
            # 获取员工信息
            member_info = staff_db.query_staff_by_id(task_assign_info.member_id_id)
            # 获取任务提交记录
            task_submit_record = task_submit_record_db.query_submit_by_tasid(tasid)
            # 获取该指派任务的所有审核人
            task_reviewers = task_review_db.query_task_reviewer_by_tmid(task_assign_info.tmid_id)
            # 获取相关审核的所有审核记录
            reviewers_record_list = []
            for item in task_reviewers:
                task_review_record = task_review_record_db.query_task_review_record_list_by_tvid_and_tasid(item.tvid,
                                                                                                       tasid)
                reviewers_record_list.append(task_review_record)
            return render(request,'task/task_review_record.html',
                      {"member_info": member_info,
                       "task_review": task_review,
                       "task_assign_info": task_assign_info,
                       "task_submit_record": task_submit_record,
                       "reviewers_record_list": reviewers_record_list})

        return render(request, "404.html")

from django.forms.models import model_to_dict
def show_assign_content(request):
    """查看任务成员的任务内容"""
    ret = {"status": False, "message":"","member_assign":'',"tags":"","attachs":""}
    tasid = request.GET.get("tasid",None)
    tasid = int(tasid)
    if tasid:
        try:
            # 根据任务分配ID获取内容
            member_assign = task_assign_db.query_task_assign_by_tasid(tasid)

            ret["member_assign"] = serializers.serialize("json", member_assign)
            # 获取标签
            tags = task_assign_tag_db.query_task_assign_tag_by_tasid(tasid)

            ret['tags'] = serializers.serialize('json', tags)
            # 获取附件
            attachs = task_assign_attach_db.query_task_assign_attach_by_tasid(tasid)

            ret['attachs'] = serializers.serialize('json', attachs)
            ret['status'] = True
        except Exception as e:
            print(e)
            ret['message'] = "查询不到相关信息"
        print("ret",ret)
    return HttpResponse(json.dumps(ret))

def task_assign_center(request):
    """任务指派中心获取所有未指派的任务"""
    is_assign = 0
    type = request.GET.get("type",0)
    query_sets = task_db.query_task_lists()
    if type:
        query_sets = query_sets.filter(type_id=type).all()
    return render(request, 'task/task_assign_center.html',  {"query_sets": query_sets,"type":type})


def department_staff(request):
    """根据部门获取员工"""
    ret = {"status": False, "data": '',"message": ''}
    dpid = request.GET.get("dpid", None)
    if dpid:
        try:
            if int(dpid) == 0:
                dp_staff_list = staff_db.query_staff_list()
            else:
                dp_staff_list = staff_db.query_staff_by_department_id(dpid)
            # 序列化queryset对象
            dp_staff_list = serializers.serialize("json", dp_staff_list)
            ret['status'] = True
            ret["data"] = dp_staff_list
        except Exception as e:
            ret["message"] = "出错了"
    else:
        ret["message"] = "请选择相应的部门"
    return HttpResponse(json.dumps(ret))


def task_sort_list(request):
    """绩效列表"""
    query_sets = task_type_db.query_task_type_list()

    return render(request, "task/task_sort_list.html", {"query_sets": query_sets})


def task_sort_edit(request):
    """"任务工单添加或编辑"""
    method = request.method
    if method == "GET":
        tpid = request.GET.get("tpid", '')
        # 有则为编辑 ,无则添加
        if tpid:
            task_sort_obj = task_type_db.query_task_type_by_id(tpid)
        else:
            tpid = 0
            task_sort_obj = []
        return render(request, 'task/task_sort_edit.html', {"task_sort_obj": task_sort_obj, "tpid": tpid})
    else:
        form = TaskSortForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            pid = request.POST.get("tpid", None)
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if pid:
                try:
                    record = task_type_db.query_task_type_by_id(pid)
                    final_info = compare_fields(TaskType._update, record, data)
                    if final_info:
                        final_info["tpid"] = pid
                        task_type_db.update_task_type(final_info)
                    ret['status'] = True
                    ret["data"] = pid
                except Exception as e:
                    ret['message'] = "更新失败"
            else:
                try:
                    task_type_db.insert_task_type(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def task_sort_delete(request):
    """任务分类删除"""
    ret = {'status': '', "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        with transaction.atomic():
            task_type_db.mutil_delete_task_type(id_list)
            ret['status'] = True
    except Exception as e:
        ret['message'] = '删除失败'
    return HttpResponse(json.dumps(ret))


def performence_display(request):
    """绩效列表"""
    query_sets = performence_db.query_performence_list()

    return render(request, "task/perfor_list.html", {"query_sets": query_sets})


def performence_statistic(request):
    """绩效统计"""
    today = datetime.date.today()
    year_month = today.strftime("%Y-%m")
    dpid = request.GET.get('dpid', 0)
    sid = request.GET.get("sid", 0)
    startMonth = is_valid_date(request.GET.get("startMonth", ''))
    endMonth = is_valid_date(request.GET.get("endMonth", ''))
    if not startMonth:
        startMonth = year_month
    if not endMonth:
        endMonth = startMonth
    if endMonth < startMonth:
        startMonth,endMonth = endMonth,startMonth
    first_day,last_day = getMonthFirstDayAndLastDay(startMonth,endMonth)
    # 构造过滤字典
    filter = build_statistic_filter(dpid,sid,first_day,last_day)
    perfor_records = performance_record_db.query_total_score(filter)
    return render(request, "task/perfor_statistic.html", {"perfor_records":perfor_records, "dpid":dpid, "sid":sid , "startMonth":startMonth , "endMonth": endMonth})


def perfor_statistic_detail(requset):
    """个人绩效详细"""
    sid = requset.GET.get("sid",0)
    today = datetime.date.today()
    year_month = today.strftime("%Y-%m")
    startMonth = requset.GET.get("startMonth",year_month)
    endMonth = requset.GET.get("endMonth",year_month)
    if not startMonth:
        startMonth = year_month
    if not endMonth:
        endMonth = startMonth
    if endMonth < startMonth:
        startMonth, endMonth = endMonth, startMonth
    first_day,last_day = getMonthFirstDayAndLastDay(startMonth,endMonth)
    query_sets = performance_record_db.query_perfor_score_by_sid(sid,first_day,last_day)
    return render(requset,'task/perfor_statistic_detail.html',{"query_sets":query_sets, "sid":sid , "startMonth":startMonth , "endMonth": endMonth})


def performence_edit(request):
    """"绩效添加或编辑"""
    method = request.method
    if method == "GET":
        pid = request.GET.get("pid", None)
        # 有则为编辑 ,无则添加
        if pid:
            performence_obj = performence_db.query_performence_by_pid(pid)
        else:
            pid = 0
            performence_obj = []
        return render(request, 'task/perfor_edit.html', {"performence_obj": performence_obj, "pid": pid})
    else:
        form = PerformForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            pid = request.POST.get("pid", None)
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if pid:
                try:
                    record = performence_db.query_performence_by_pid(pid)
                    final_info = compare_fields(Performance._update, record, data)
                    if final_info:
                        final_info["pid"] = pid
                        performence_db.update_performence(final_info)
                    ret["data"] = pid
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    performence_db.insert_performence(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def performence_delete(request):
    """绩效删除"""
    ret = {'status': '', "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        with transaction.atomic():
            performence_db.mutil_delete_performence(id_list)
            ret['status'] = True
    except Exception as e:
        ret['message'] = '删除失败'
    return HttpResponse(json.dumps(ret))


def personal_task_list(request):
    """获取个人任务列表"""
    user_id = request.user.staff.sid
    filters = request.GET
    search_key = int(filters.get("s", 0))
    query_sets = task_assign_db.query_task_assign_by_member_id(user_id)
    query_sets = query_sets.filter(is_finish=search_key).all()
    return render(request, 'task/personal_task_list.html', {"query_sets": query_sets,"filter": search_key})


def personal_task_detail(request):
    """个人任务详细"""
    tasid = request.GET.get("tasid", 0)
    user_id = request.user.staff.sid
    task_assign_obj = task_assign_db.query_task_assign_by_tasid(tasid)
    task_assign_obj = task_assign_obj.first()
    return render(request, 'task/personal_task_detail.html', {"task_obj": task_assign_obj,"user_id":user_id})


def complete_task(request):
    """完成工单"""
    method = request.method
    ret = {"status": False, "data": "", "message": ""}
    if method == "GET":
        tasid = request.GET.get("tasid", None)
        if tasid:
            # 获取任务内容
            task_obj = task_assign_db.query_task_assign_by_tasid(tasid)
            task_obj = task_obj.first()
            # 获取最后一次任务提交记录的完成进度
            last_record = task_submit_record_db.query_last_submit_record(tasid)
            if last_record:
                last_completion = last_record.completion
            else:
                last_completion = 0
            # 获取任务提交历史记录
            task_submit_record = task_submit_record_db.query_submit_by_tasid(tasid)

            return render(request, 'task/complete_task.html', {
                "task_obj": task_obj,
                "task_submit_record": task_submit_record,
                "completion": last_completion})
    else:
        form = CompleteTaskForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            # 获取标签并删除
            tags = data.get("tags", None)
            tag_list = tags.split("|")
            data.pop("tags")
            # 获取附件并删除
            attachment = data.get("attachment", None)
            attachment = list(json.loads(attachment))
            data.pop("attachment")
            if data:
                # 获取完成进度
                task_assign_obj = task_assign_db.query_task_assign_by_tasid(data["tasid_id"])
                task_assign_obj = task_assign_obj.first()
                task_map_obj = task_map_db.query_task_by_tmid(task_assign_obj.tmid_id)
                try:
                    with transaction.atomic():
                        if task_assign_obj.progress > int(data["completion"]):
                            data["completion"] = task_assign_obj.progress
                        else:
                            # 更新指派任务进度
                            task_assign_obj.progress = data["completion"]
                            task_assign_obj.save()
                        tsid = task_submit_record_db.insert_task_submit_record(data)
                        # 如果任务提交记录插入成功
                        if tsid:
                            # 插入标签
                            id_dict = {"tsid_id": tsid}
                            tags_list = build_tags_info(id_dict,tag_list)
                            task_submit_tag_db.mutil_insert_tag(tags_list)
                            # 插入附件
                            attachment_list = build_attachment_info(id_dict, attachment)
                            task_submit_attach_db.mutil_insert_attachment(attachment_list)
                        # 如果任务完成，则添加到缓存里 等待审核
                        if int(data["completion"]) == 100:
                            today = datetime.datetime.today()
                            weekday = today.weekday()
                            del_day = calculate_expire_date(weekday)
                            expire_date = today + timedelta(del_day)
                            expire_date = expire_date.strftime("%Y-%m-%d %H:%M:%S")
                            k1 = "task_review"
                            k2 = data["tasid_id"]
                            if not res.hexists(k1,k2):
                                res.hset(k1,k2,expire_date)
                            # 审核通知
                            task_review_list=task_review_db.query_task_reviewer_by_tmid(task_assign_obj.tmid)
                            data_manage = {
                                'notice_title': '您有一个新的审核工单等待审核！',
                                'notice_body': task_map_obj.title,
                                'notice_url': '/task/personal/reviews/review',
                                'notice_type': 'notice',
                            }
                            for item in task_review_list:
                                sid_id = item.sid_id
                                task_assign_obj = task_assign_db.query_task_assign_by_member_id_and_tmid(sid_id,task_assign_obj.tmid)
                                if task_assign_obj:
                                    data_manage["notice_url"] += "?tasid={0}".format(task_assign_obj.tasid)
                                notice_add(sid_id, data_manage)
                        ret["status"] = True
                except Exception as e:
                    print(e)
                    ret["message"] = "提交失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def attachment_upload(request):
    """附件上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    target_path = "media/upload/task"
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    try:
        # 获取文件对象
        file_obj = request.FILES.get("file")
        raw_name = file_obj.name
        postfix = raw_name.split(".")[-1]
        if not file_obj:
            pass
        else:
            file_name = str(uuid.uuid4())+"."+postfix
            # 查看路径是否存在，没有则生成
            if not os.path.exists(os.path.dirname(target_path)):
                os.makedirs(target_path)
            file_path = os.path.join(target_path, file_name)
            # os.path.join()在Linux/macOS下会以斜杠（/）分隔路径，而在Windows下则会以反斜杠（\）分隔路径,
            # 故统一路径将'\'替换成'/'
            file_path = file_path.replace('\\', "/")
            with open(file_path, "wb") as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
            ret["status"] = True
            ret["data"]['path'] = file_path
            ret["data"]['name'] = raw_name
    except Exception as e:
        ret["summary"] = str(e)
    return HttpResponse(json.dumps(ret))


def attachment_download(request):
    name = request.GET.get("name", None)
    file_path = request.GET['url']

    def file_iterator(file_path, chunk_size=512):
        with open(file_path, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    response = StreamingHttpResponse(file_iterator(file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(name.encode('utf-8').decode('ISO-8859-1'))
    return response