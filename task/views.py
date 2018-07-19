import json
import os
import uuid
import re
from django.core import serializers
from django.db import transaction
from django.http import StreamingHttpResponse
from django.shortcuts import render, HttpResponse,redirect
from task.forms.form import TaskForm, PerformForm, TaskAssignForm, CompleteTaskForm,TaskReviewForm,TaskSortForm,TaskMapForm
from .server import *
from .utils import build_attachment_info, build_tags_info, build_reviewer_info, compare_json,build_assign_tags_info,build_assign_attach_info

# Create your views here.



def index(request):
    return render(request,'index_v3.html')


def publish_task(request):
    """创建任务"""
    method = request.method
    if method == "GET":
        return render(request, "task/task_edit.html", {"tid": 0})
    else:
        ret = {"status": False, "data": "", "message": ""}
        form = TaskForm(data=request.POST)
        if form.is_valid():
            data = request.POST
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
                        tid = task_db.insert_task(data)
                        # 如果任务插入成功
                        if tid:
                            # 插入标签
                            id_dict = {"tid_id": tid}
                            tags_list = build_tags_info(id_dict, tag_list)
                            task_tag_db.mutil_insert_tag(tags_list)
                            # 插入附件
                            attachment_list = build_attachment_info(id_dict, attachment)
                            task_attachment_db.mutil_insert_attachment(attachment_list)
                            ret["status"] = True
                except Exception as e:
                    print(e)
                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def task_edit(request):
    """任务编辑"""
    method = request.method
    if method == "GET":
        tid = request.GET.get("tid", None)
        if tid:
            # 获取任务信息及其标签信息、附件信息、审核人
            task_info = task_db.query_task_by_tid(tid)
            task_tag_info = task_tag_db.query_task_tag_by_tid(tid)
            task_attachment_info = task_attachment_db.query_task_attachment_by_tid(tid)
            return render(request, 'task/task_edit.html',
                      {"tid": tid,
                       "task_info": task_info,
                       "task_tag_info": task_tag_info,
                       "task_attachment_data": task_attachment_info,}
                          )
        return HttpResponse(json.dumps({"status": "False", "message": "找不到相关信息"}))
    else:
        ret = {"status": False, "data": "", "message": ""}
        form = TaskForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            # 获取任务id
            tid = data.get("tid", None)
            # 获取标签并删除
            tags = data.get("tags", None)
            data.pop("tags")
            tag_list = list(json.loads(tags))
            # 获取附件并删除
            attachment = data.get("attachment", None)
            data.pop("attachment")
            attachment_list = list(json.loads(attachment))
            # 获取审核人并删除
            reviewers = data.get("reviewers", None)
            reviewers_list = list(json.loads(reviewers))
            data.pop("reviewers")
            if tid:
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
                        # 更新审核人
                        reviewer_record = task_review_db.query_task_reviewer_by_tid(tid)
                        insert_review, update_review, delete_id_review = compare_json(reviewer_record, reviewers_list,'tvid')
                        if insert_review:
                            task_review_db.mutil_insert_reviewer(insert_review)
                        if update_review:
                            task_review_db.mutil_update_reviewer(update_review)
                        if delete_id_review:
                            task_review_db.mutil_delete_reviewer(delete_id_review)
                        ret['status'] = True
                except Exception as e:
                    print(e)
                    ret["message"] = str(e)
        return HttpResponse(json.dumps(ret))



def task_detail(request):
    tmid = request.GET.get("tmid", None)
    task_obj = task_map_db.query_task_by_tmid(tmid)
    return render(request, 'task/task_detail.html', {"task_obj": task_obj})


def task_base_detail(request):
    tid = request.GET.get("tid", None)
    # 据任务分配ID获取内容
    task_obj = task_db.query_task_by_tid(tid)
    return render(request, 'task/task_base_detail.html', {"task_obj": task_obj})


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
    print(ids)
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    print(id_list)
    status = {"status": 0}
    try:
        task_db.multi_delete_task(id_list, status)
        ret['status'] = True
    except Exception as e:
        print(e)
        ret['status'] = "删除失败"
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
    method = request.method
    if method == "GET":
        team = request.GET.get('team', None)
        tids = request.GET.get("tids",None)
        if tids:
            tid_list = tids.split("|")
            # 转化成数字
            id_list = []
            for item in tid_list:
                if item:
                    id_list.append(int(item))
            query_sets = task_db.query_task_by_tids(id_list)
            return render(request,'task/task_assign.html',{"query_sets":query_sets,"team":team,"tids":tids})
    else:
        ret = {"status": False, "data": "", "message": ''}
        data = request.POST
        form =TaskMapForm(data=data)
        if form.is_valid():
            # 获取任务id并删除
            data=data.dict()
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
                data['tid_id'] = int(tid)
                task_list.append(data)
            try:
                with transaction.atomic():
                    for modify in task_list:
                        tmid = task_map_db.insert_task(modify)
                        # 插入指派对象
                        assigner_list = []
                        for item in assigners:
                            item['tmid_id'] = tmid
                            assigner_list.append(item)
                        print(assigner_list)
                        task_assign_db.mutil_insert_task_assign(assigner_list)
                        # 插入审核人
                        reviewers_list =[]
                        for item in reviewers:
                            item['tmid_id'] = tmid
                            reviewers_list.append(item)
                        task_review_db.mutil_insert_reviewer(reviewers_list)
                    ret['status'] = True
            except Exception as e:
                print(e)
                ret["message"] = "指派失败"
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
                        # print(tags_assign_list)
                        task_assign_tag_db.mutil_insert_assign_tag(tags_assign_list)
                        # 插入附件
                        attachment_list = build_assign_attach_info(tasid, attachment)
                        task_assign_attach_db.mutil_insert_assign_attach(attachment_list)
                        ret["status"] = True
                except Exception as e:
                    print(e)
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
    user_id = 1
    if method == "GET":
        filter = request.GET
        type_id = int(filter.get("s", 0))
        # 根据用户id去获取审核任务
        task_review = task_review_db.query_task_reviewer_by_sid(user_id)
        tmid_list = []
        for item in task_review:
            print(item)
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
        user_id = 1
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
    else:
        ret = {'status': False, 'message':'', 'data':''}
        data = request.POST
        form = TaskReviewForm(data=data)
        if form.is_valid():
            try:
                data = data.dict()
                task_review_record_db.insert_review_record(data)
                is_complete = data["is_complete"]
                # 如果通过 更新相应任务的完成状态
                is_finish = True
                if is_complete:
                    # check 是否所有审核人都确认通过
                    # 获取任务id
                    task_assign_obj = task_assign_db.query_task_assign_by_tasid(data['tasid_id'])
                    task_assign_obj=task_assign_obj.first()
                    # 获取任务审核人
                    task_review_list = task_review_db.query_task_reviewer_by_tmid(task_assign_obj.tmid_id)
                    # 遍历该所有审核人对其的记录
                    for item in task_review_list:
                        last_review_record = task_review_record_db.query_task_review_record_last_by_tvid_and_tasid(item.tvid,data['tasid_id'])
                        if not last_review_record:
                            is_finish = False
                            break
                        else:
                            if not last_review_record.is_complete:
                                is_finish = False
                                break
                    if is_finish:
                        # 更新任务为通过状态
                        query_sets = task_assign_db.query_task_assign_by_tasid(data["tasid_id"])
                        query_sets.update(is_finish=1)
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


def show_assign_content(request):
    """查看任务成员的任务内容"""
    ret = {"status": False, "message":"","member_assign":'',"tags":"","attachs":""}
    tasid = request.GET.get("tasid",None)
    tasid = int(tasid)
    if tasid:
        try:
            # 根据任务分配ID获取内容
            member_assign = task_assign_db.query_task_assign_by_tasid(tasid)
            ret["member_assign"] =serializers.serialize("json", member_assign)
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
        print(ret)
    return HttpResponse(json.dumps(ret))


def task_assign_center(request):
    """任务指派中心获取所有未指派的任务"""
    is_assign = 0
    query_sets = task_db.query_task_lists()
    return render(request, 'task/task_assign_center.html',  {"query_sets": query_sets})


def department_staff(request):
    """根据部门获取员工"""
    ret = {"status": False, "data": '',"message": ''}
    dpid = request.GET.get("dpid", None)
    if dpid:
        try:
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
    """"绩效添加或编辑"""
    method = request.method
    if method == "GET":
        tpid = request.GET.get("tpid", None)
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
                    task_type_db.update_task_type(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
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

    return render(request, "task/performence.html", {"query_sets": query_sets})


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
        return render(request, 'task/performence_edit.html', {"performence_obj": performence_obj, "pid": pid})
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
                    performence_db.update_performence(data)
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
    user_id = 1
    filters = request.GET
    search_key = int(filters.get("s", 0))
    print(search_key)
    query_sets = task_assign_db.query_task_assign_by_member_id(user_id)
    query_sets = query_sets.filter(is_finish=search_key).all()
    return render(request, 'task/personal_task_list.html', {"query_sets": query_sets,"filter": search_key})


def personal_task_detail(request):
    tasid = request.GET.get("tasid", 0)
    print("tasid",tasid)
    user_id = 1
    task_assign_obj = task_assign_db.query_task_assign_by_tasid(tasid)
    task_assign_obj = task_assign_obj.first()
    return render(request, 'task/personal_task_detail.html', {"task_obj": task_assign_obj,"user_id":user_id})


def complete_task(request):
    """任务提交记录"""
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
            data.pop("attachment")
            print(data)
            if data:
                # 获取完成进度
                task_assign_obj = task_assign_db.query_task_assign_by_tasid(data["tasid_id"])
                task_assign_obj = task_assign_obj.first()
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
                            ret["status"] = True
                except Exception as e:
                    print(e)
                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def attachment_upload(request):
    """附件上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    try:
        # 获取文件对象
        file_obj = request.FILES.get("file")
        raw_name = file_obj.name
        if not file_obj:
            pass
        else:
            file_name = str(uuid.uuid4())
            file_path = os.path.join("static/upload/task", file_name)
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