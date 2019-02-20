import os
import uuid
from django.shortcuts import render, HttpResponse
from django.db.models import Q
from django.forms.models import model_to_dict
from django.db import transaction
from django.core import serializers
from task.templatetags.admin_tags import change_to_task_type,change_to_staff,change_to_department
from personnel.server import staff_db
from .forms.form import KnowledgeForm
from common.functions import filter_fields,build_attachment_info,compare_fields,compare_json

import json
from task.server import task_submit_record_db,task_submit_attach_db,\
    task_submit_tag_db,task_assign_db,task_map_tag_db,task_map_db
from .server import *
from common.functions import CJSONEncoder

# Create your views here.


def collect(request):
    """知识收录"""
    origin_id = request.GET.get("tsid",None)
    ret = {"status": False,"data":""}
    user = request.user.staff.sid
    origin_obj = coll_record_db.query_record_by_origin(origin_id)
    if not origin_obj:
        try:
            with transaction.atomic():
                # 获取记录信息
                record_obj = task_submit_record_db.query_record_by_id(origin_id)
                if record_obj:
                    record_tags = task_submit_tag_db.query_task_tag_by_tsid(origin_id)
                    record_attach = task_submit_attach_db.query_task_submit_attachment_by_tsid(origin_id)
                    # 获取工单信息
                    task_assgin_obj = task_assign_db.query_task_assign_by_tasid(record_obj.tasid_id)
                    task_map_obj = task_map_db.query_task_by_tmid(task_assgin_obj.first().tmid_id)
                    map_tags = task_map_tag_db.query_tag_by_tmid(task_map_obj.tmid)
                    contributor = task_assgin_obj.first().member_id_id
                    # 在构造收录信息
                    tag = ""
                    for item in record_tags:
                        tag += item.name + ';'
                    relate_tag = ""
                    for item in map_tags:
                        relate_tag += item.name + ';'
                    relate_title = task_map_obj.title
                    insert_info = {
                        "origin": origin_id,
                        "title": record_obj.title,
                        "summary": record_obj.summary,
                        "remark": record_obj.remark,
                        "tag": tag,
                        "relate_tag": relate_tag,
                        "relate_title": relate_title,
                        "recorder_id": user,
                        "contributor_id": contributor,
                        "type_id": task_map_obj.type_id,
                        "tid_id": task_map_obj.tid_id
                        }
                    tsid = coll_record_db.insert_record(insert_info)
                    # 收录附件
                    att_list = []
                    for obj in record_attach:
                        att_json = {}
                        att_json["tsid_id"] = tsid
                        att_json["attachment"] = obj.attachment
                        att_json["description"] = obj.description
                        att_json["name"] = obj.name
                        att_list.append(att_json)
                    if att_list:
                        record_attach_db.mutil_insert_attachment(att_list)
                    # 原数据更改为收录状态
                    task_submit_record_db.update_status({"tsid":origin_id,"is_collected":1})
                    ret['status'] = True
        except Exception as e:
            print(e)
    else:
        ret = {"status": True, "data": ""}
    return HttpResponse(json.dumps(ret))


def collect_delete(request):
    """删除收录"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        with transaction.atomic():
            coll_record_db.multi_delete(id_list)
            # 删除附件
            record_attach_db.mutil_delete(id_list)
            ret['status'] = True
    except Exception as e:
        print(e)
        ret['message'] = "删除失败"
    return HttpResponse(json.dumps(ret))


def collections(request):
    """知识库中心"""
    type_ = request.GET.get("type",0)
    query_sets = coll_record_db.query_record_list()
    if type_:
        query_sets = coll_record_db.query_record_by_type(type_)
    return render(request,"collections/collections.html",{"query_sets":query_sets,"type":type_})


def knowledge(request):
    """指引匹配"""
    tmid = int(request.GET.get("tmid",0))
    ret = {"status":False,"data":[]}
    if tmid:
        map_obj = task_map_db.query_task_by_tmid(tmid)
        map_tag_list = task_map_tag_db.query_tag_by_tmid(tmid)
        title = map_obj.title
        type = map_obj.type_id
        query_sets = coll_record_db.query_record_by_type(type)
        if query_sets:
            q_obj = Q()
            q_obj.connector = "OR"
            # 构造标签Q
            if map_tag_list:
                _tag_fields = CollRecord._tag_field
                for item in map_tag_list:
                    q_obj.children.append(("%s__icontains" % _tag_fields, item.name))
            # 构造标题Q
            _title_field = CollRecord._title_field
            q_obj.children.append(("%s__icontains" % _title_field, title))
            db_result = query_sets.filter(q_obj).order_by("favor").all()
            data = serializers.serialize("json", db_result)
            data = json.loads(data)
            for item in data:
                item["fields"]["type"] = change_to_task_type(item["fields"]["type"])
            ret["status"] = True
            ret["data"] = data
    return HttpResponse(json.dumps(ret))


def knowledge_detail(request):
    """指引详细"""
    id = request.GET.get("id", None)
    uid = request.user.staff.sid
    ret = {"status": False, "data": "", "signal":False}
    if id:
        try:
            # record_obj = coll_record_db.query_record_by_id(id)
            record_obj = CollRecord.objects.filter(nid=id).first()
            if record_obj:
                # 格式化数据
                record_json = {}
                print("record_json",record_obj.__dict__)
                # del record_json['_state']
                record_json["nid"] = record_obj.nid
                record_json["type_id"] = record_obj.type.name
                record_json["recorder_id"] = record_obj.recorder.name
                contributor_id = record_obj.contributor_id
                staff_obj = staff_db.query_staff_by_id(contributor_id)
                record_json["contributor_id"] = record_obj.contributor.name
                record_json["depart"] = change_to_department(staff_obj.department_id)
                record_json["phone"] = staff_obj.phone
                record_json["title"]=record_obj.title
                record_json["tag"]=record_obj.tag
                record_json["create_time"]=record_obj.create_time
                record_json["favor"] = record_obj.favor
                record_json["summary"]=record_obj.summary
                record_json["remark"] = record_obj.remark
                record_attach = record_attach_db.query_record_attach_by_tsid(id)
                if record_attach:
                    record_json['attach'] = serializers.serialize("json", record_attach)
                else:
                    record_json['attach'] = ''
                # 获取点赞状态
                is_exist = coll_favor_db.is_exist({"tsid_id":id, "uid_id":uid})
                if is_exist:
                    obj = is_exist.first()
                    if obj.status:
                        ret['signal'] = True
                ret['status'] = True
                ret['data'] = record_json
                print("detail",ret)
                return HttpResponse(json.dumps(ret,cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request, '404.html')


def knowledge_edit(request):
    """自定义添加知识"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", '')
        if id:
            query_set = coll_record_db.query_record_by_id(id)
            know_attach = record_attach_db.query_record_attach_by_tsid(id)
            if not know_attach:
                know_attach = ''
            return render(request,"collections/knowledge_edit.html",{"query_set":query_set ,"nid": id, "know_attach": know_attach})
        else:
            return render(request,'404.html')
    else:
        ret = {'status': False, "data": '', "message": ""}
        form = KnowledgeForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            k_attach = data.get("attach", '')
            id = data.get("id",None)
            k_attach = list(json.loads(k_attach))
            if not id:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入收录知识信息
                        coll_info = filter_fields(CollRecord._insert, data)
                        nid = coll_record_db.insert_record(coll_info)
                        # 插入知识附件
                        if k_attach:
                            k_attach = build_attachment_info({"tsid_id": nid}, k_attach)
                            record_attach_db.mutil_insert_attachment(k_attach)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "添加失败"
            else:
                try:
                    with transaction.atomic():
                        # 更新收录信息
                        record = coll_record_db.query_record_by_id(id)
                        know_info = compare_fields(CollRecord._update, record, data)
                        if know_info:
                            know_info["nid"] = id
                            coll_record_db.update_info(know_info)
                        # 更新附件
                        if k_attach:
                            att_record = record_attach_db.query_record_attach_by_tsid(id)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, k_attach, "nid")

                            if insert_att:
                                insert_att = build_attachment_info({"tsid_id": id}, insert_att)
                                record_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                record_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                record_attach_db.mutil_delete(delete_id_att)
                        else:
                            record_attach_db.mutil_delete_by_tsid(id)
                        ret['data'] = id
                        ret['status'] = True
                except Exception as e:
                    print(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def knowledge_favor(request):
    """点赞收录"""
    print("id",request.GET.get("id",0))
    id = int(request.GET.get("id",0))
    uid = int(request.GET.get("user",0))
    ret = {"status":False,"data":""}
    signal = True
    if id and uid:
        info = {"tsid_id":id, "uid_id":uid}
        is_exist = coll_favor_db.is_exist(info)
        if is_exist:
            obj = is_exist.first()
            if not obj.status:
                obj.status = 1
                obj.save()
            else:
                obj.status = 0
                signal = False
            obj.save()
        else:
            coll_favor_db.insert_favor(info)
        # 更新点赞数
        row = coll_favor_db.count_favor(id)
        favor_count = int(row[0])
        refer_obj = coll_record_db.query_record_by_id(id)
        refer_obj.favor = favor_count
        refer_obj.save()
        ret["data"] = {"count":favor_count,"signal":signal}
        ret["status"] = True
    return HttpResponse(json.dumps(ret))


def know_attach(request):
    """收录附件上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/collection/"
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
            file_name = str(uuid.uuid4()) + "." + postfix
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

