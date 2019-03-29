from django.shortcuts import render
from assets.server import *
from personnel.server import *
from assets.forms.form import *
import json
from django.db import transaction
from common.functions import filter_fields,build_attachment_info,compare_fields,compare_json
from django.shortcuts import render, HttpResponse
from personnel.templatetags.personnel_tags import *
from sfa.templatetags.sfa_tags import *
from django.core import serializers
from common.functions import *

# Create your views here.

def assets(request):
    company_id = int(request.GET.get("company", 6))
    project_id = int(request.GET.get("project", 3))
    query_sets = assets_db.query_assets_by_list()
    if company_id < 6:
        query_sets = query_sets.filter(company_id=company_id)
    if project_id < 3:
        query_sets = query_sets.filter(project_id=project_id)
    return render(request, "assets/assets.html",
                  {"query_sets": query_sets, "company": company_id, "project": project_id})

def assets_edit(request):
    mothod = request.method
    print('mothod', mothod)
    if mothod == "GET":
        nid = request.GET.get("nid", "")
        print('request', request.GET)
        if nid:
            # 更新
            query_sets = assets_db.query_assets_by_id(nid)
            assets_attach = assetsattach_db.query_assets_attachment_by_sid(nid)
            if not assets_attach:
                assets_attach = ""
        else:
            query_sets = {}
            assets_attach = {}
        return render(request, "assets/assets_edit.html", {"query_set": query_sets,
                                                            "assets_attach": assets_attach,
                                                            "sid": nid})
    else:
        ret = {'status': False, "data": '', "message": ""}
        print('data', ret)
        form = AssetsForm(data=request.POST)
        print("request.POST", request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            assets_attach = data.get("attach", '')
            nid = data.get("sid", None)
            assets_attach = list(json.loads(assets_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新收支管理
                        record = assets_db.query_assets_by_id(nid)
                        assets_info = compare_fields(Assets._update, record, data)
                        if assets_info:
                            assets_info["nid"] = nid
                            assets_db.update_info(assets_info)
                        if assets_attach:
                            # 更新附件
                            att_record = assetsattach_db.query_assets_attachment_by_sid(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, assets_attach, "said")
                            if insert_att:
                                insert_att = build_attachment_info({"sid_id": nid}, insert_att)
                                assetsattach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                assetsattach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                assetsattach_db.mutil_delete_task_attachment(delete_id_att)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        assets_info = filter_fields(Assets._insert, data)
                        sid = assets_db.insert_info(assets_info)
                        if assets_attach:
                            assets_attach = build_attachment_info({"sid_id": sid}, assets_attach)
                            assetsattach_db.mutil_insert_attachment(assets_attach)
                        ret['status'] = True
                        ret['data'] = sid
                except Exception as e:
                    print(e)
                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))

def assets_detail(request):
    id = request.GET.get("id", None)
    ret = {"status": False, "data": "", "message": ""}
    if id:
        try:
            assets_obj = assets_db.query_assets_by_id(id)
            if assets_obj:
                # 格式化数据
                assets_json = assets_obj.__dict__
                assets_json.pop('_state')
                assets_json["company_id"] = change_to_company(assets_json["company_id"])
                assets_json["project_id"] = change_to_project(assets_json["project_id"])
                assets_json["assets_classify_id"] = change_to_assets_classify(assets_json["assets_classify_id"])
                assets_json["save_coordinate_id"] = change_to_save_coordinate(assets_json["save_coordinate_id"])
                assets_json["procurement_name_id"] = change_to_procurement(assets_json["procurement_name_id"])
                assets_json["user_name_id"] = change_to_username(assets_json["user_name_id"])
                assets_json["assets_status_id"] = change_to_assets_status(assets_json["assets_status_id"])
                assets_json["approver_id"] = change_to_approver2(assets_json["approver_id"])
                assets_attach = assetsattach_db.query_assets_attachment(id)
                if assets_attach:
                    assets_json['attach'] = serializers.serialize("json", assets_attach)
                else:
                    assets_json['attach'] = ''
                ret['status'] = True
                ret['data'] = assets_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request, '404.html')

def assets_delete(request):
    """删除资产管理"""
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
            assets_db.multi_delete(id_list)
            # 删除附件
            assetsattach_db. multi_delete_attach_by_edit_id(id_list)
            ret['status'] = True
    except Exception as e:
        print(e)
        ret['message'] = "删除失败"
    return HttpResponse(json.dumps(ret))

def assets_detail_1(request):
    cid = request.GET.get("nid", None)
    id = 1
    if cid:
        query_sets = assets_db.query_assets_by_id(cid)
        query_set = supplies_db.query_supp_by_id(id)
        get_sets = suppliesreturn_db.query_supp_by_id(id)
        if query_sets:
            assets_attach = assetsattach_db.query_assets_attachment(cid)
            if not assets_attach:
                assets_attach = ''
            return render(request, "assets/assets_detail.html", {"query_set": query_sets,
                                                                 "query_sets": query_set,
                                                                 "get_sets": get_sets,
                                                                "assets_attach": assets_attach,
                                                                })
    return render(request, '404.html')


def assets_detail_2(request):
    id = request.GET.get("id", None)
    ret = {"status": False, "data": "", "message": ""}
    if id:
        try:
            assets_obj = supplies_db.query_supp_by_id(id)
            if assets_obj:
                # 格式化数据
                assets_json = assets_obj.__dict__
                assets_json.pop('_state')
                assets_json["supplies_id_id"] = change_to_supplies(assets_json["supplies_id_id"])
                assets_json["sid_id"] = change_to_staff(assets_json["sid_id"])
                assets_attach = assetsattach_db.query_assets_attachment(id)
                if assets_attach:
                    assets_json['attach'] = serializers.serialize("json", assets_attach)
                else:
                    assets_json['attach'] = ''
                ret['status'] = True
                ret['data'] = assets_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request, '404.html')


def assets_detail_3(request):
    id = request.GET.get("id", None)
    ret = {"status": False, "data": "", "message": ""}
    if id:
        try:
            assets_obj = suppliesreturn_db.query_supp_by_id(id)
            if assets_obj:
                # 格式化数据
                assets_json = assets_obj.__dict__
                assets_json.pop('_state')
                assets_json["supplies_id_id"] = change_to_supplies(assets_json["supplies_id_id"])
                assets_json["sid_id"] = change_to_staff(assets_json["sid_id"])
                assets_attach = assetsattach_db.query_assets_attachment(id)
                if assets_attach:
                    assets_json['attach'] = serializers.serialize("json", assets_attach)
                else:
                    assets_json['attach'] = ''
                ret['status'] = True
                ret['data'] = assets_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request, '404.html')