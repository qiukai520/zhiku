from django.shortcuts import render,HttpResponse
from django.db import transaction
import json
from task.server import task_submit_record_db,task_submit_attach_db,\
    task_submit_tag_db,task_assign_db,task_map_tag_db,task_map_db
from .server import *

# Create your views here.


def collect(request):
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
                        "recorder_id":user,
                        "type_id":task_map_obj.type_id,
                        "tid_id":task_map_obj.tid_id
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
