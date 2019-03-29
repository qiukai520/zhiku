from django.shortcuts import render
from revenue.server import *
from revenue.forms.form import *
import json
import os
import uuid
from django.db import transaction
from common.functions import filter_fields,build_attachment_info,compare_fields,compare_json
from django.shortcuts import render, HttpResponse
from personnel.templatetags.personnel_tags import *
from django.core import serializers
from common.functions import *

# Create your views here.

def income(request):
    """收入管理"""
    company_id = int(request.GET.get("company", 6))
    project_id = int(request.GET.get("project", 3))
    query_sets = revenue_db.query_revenue_by_list()
    if company_id < 6:
        query_sets = query_sets.filter(company_id=company_id)
    if project_id < 3:
        query_sets = query_sets.filter(project_id=project_id)
    return render(request, "revenue/income.html", {"query_sets": query_sets, "company": company_id, "project": project_id})

def income_edit(request):
    mothod = request.method
    print('mothod',mothod)
    if mothod == "GET":
        nid = request.GET.get("nid", "")
        print('request',request.GET)
        if nid:
            # 更新
            query_sets = revenue_db.query_revenue_by_id(nid)
            revenue_info = revenue_db.query_revenue_by_type(nid)
            revenue_attach = revenueattach_db.query_revenue_attachment_by_sid(nid)
            if not revenue_attach:
                revenue_attach = ""
        else:
            query_sets = {}
            revenue_info = {}
            revenue_attach = {}
        return render(request, "revenue/income_edit.html", {"query_set": query_sets,
                                                             "revenue_attach": revenue_attach,
                                                            "revenue_info": revenue_info,
                                                             "sid": nid})
    else:
        ret = {'status': False, "data": '', "message": ""}
        print('data',ret)
        form = RevenueForm(data=request.POST)
        print("request.POST",request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            revenue_attach = data.get("attach", '')
            nid = data.get("sid", None)
            revenue_attach = list(json.loads(revenue_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新收支管理
                        record = revenue_db.query_revenue_by_id(nid)
                        revenue_info = compare_fields(Revenue._update, record, data)
                        if revenue_info:
                            revenue_info["nid"] = nid
                            revenue_db.update_info(revenue_info)
                        if revenue_attach:
                            # 更新附件
                            att_record = revenueattach_db.query_revenue_attachment_by_sid(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, revenue_attach, "said")
                            if insert_att:
                                insert_att = build_attachment_info({"sid_id": nid}, insert_att)
                                revenueattach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                revenueattach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                revenueattach_db.mutil_delete_task_attachment(delete_id_att)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        revenue_info = filter_fields(Revenue._insert, data)
                        sid = revenue_db.insert_info(revenue_info)
                        if revenue_attach:
                            revenue_attach = build_attachment_info({"sid_id": sid}, revenue_attach)
                            revenueattach_db.mutil_insert_attachment(revenue_attach)
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

def income_delete(request):
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
            revenue_db.multi_delete(id_list)
            # 删除附件
            revenueattach_db. multi_delete_attach_by_edit_id(id_list)
            ret['status'] = True
    except Exception as e:
        print(e)
        ret['message'] = "删除失败"
    return HttpResponse(json.dumps(ret))

def revenue_attach(request):
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path="media/upload/revenue/attach"
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


def income_detail(request):
    cid = request.GET.get("nid", None)
    if cid:
        query_sets = revenue_db.query_revenue_by_id(cid)
        if query_sets:
            # customer_licence = customer_licence_db.query_customer_licence(cid)
            life_attach = revenueattach_db.query_revenue_attachment_by_sid(cid)
            if not life_attach:
                customer_attach = ''
            return render(request, "revenue/income_detail.html", {"query_set": query_sets,
                                                                   "life_attach": life_attach,
                                                                   })
    return render(request, '404.html')

def income_detail_1(request):
    id = request.GET.get("id", None)
    ret = {"status": False, "data": "", "message": ""}
    if id:
        try:
            revenue_obj = revenue_db.query_revenue_by_id(id)
            if revenue_obj:
                # 格式化数据
                revenue_json = revenue_obj.__dict__
                revenue_json.pop('_state')

                revenue_json["company_id"] = change_to_company(revenue_json["company_id"])
                revenue_json["project_id"] = change_to_project(revenue_json["project_id"])
                revenue_json["income_classify_id"] = change_to_incomeclassify(revenue_json["income_classify_id"])
                revenue_json["associates_id"] = change_to_associates(revenue_json["associates_id"])
                revenue_json["approver_id"] = change_to_approver2(revenue_json["approver_id"])
                revenue_attach = revenueattach_db.query_revenue_attachment(id)
                if revenue_attach:
                    revenue_json['attach'] = serializers.serialize("json", revenue_attach)
                else:
                    revenue_json['attach'] = ''
                ret['status'] = True
                ret['data'] = revenue_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request, '404.html')


#支出管理
def disbursement(request):
    """支出管理"""
    company_id = int(request.GET.get("company", 6))
    project_id = int(request.GET.get("project", 3))
    query_sets = disbur_db.query_disbur_by_list()
    if company_id < 6:
        query_sets = query_sets.filter(company_id=company_id)
    if project_id < 3:
        query_sets = query_sets.filter(project_id=project_id)
    return render(request, "revenue/disbursement.html", {"query_sets": query_sets, "company": company_id, "project": project_id})

def disbursement_edit(request):
    mothod = request.method
    print('mothod', mothod)
    if mothod == "GET":
        nid = request.GET.get("nid", "")
        print('request', request.GET)
        if nid:
            # 更新
            query_sets = disbur_db.query_disbur_by_id(nid)
            disbur_attach = disburattach_db.query_disbur_attachment_by_sid(nid)
            if not disbur_attach:
                disbur_attach = ""
        else:
            query_sets = {}
            disbur_attach = {}
        return render(request, "revenue/disbursement_edit.html", {"query_set": query_sets,
                                                            "disbur_attach": disbur_attach,
                                                            "sid": nid})
    else:
        ret = {'status': False, "data": '', "message": ""}
        print('data', ret)
        form = DisbursementForm(data=request.POST)
        print("request.POST", request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            disbur_attach = data.get("attach", '')
            nid = data.get("sid", None)
            disbur_attach = list(json.loads(disbur_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新收支管理
                        record = disbur_db.query_disbur_by_id(nid)
                        disbur_info = compare_fields(Disbursement._update, record, data)
                        if disbur_info:
                            disbur_info["nid"] = nid
                            disbur_db.update_info(disbur_info)
                        if disbur_attach:
                            # 更新附件
                            att_record = disburattach_db.query_disbur_attachment_by_sid(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, disbur_attach, "said")
                            if insert_att:
                                insert_att = build_attachment_info({"sid_id": nid}, insert_att)
                                disburattach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                disburattach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                disburattach_db.mutil_delete_task_attachment(delete_id_att)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        disbur_info = filter_fields(Disbursement._insert, data)
                        sid = disbur_db.insert_info(disbur_info)
                        if disbur_attach:
                            disbur_attach = build_attachment_info({"sid_id": sid}, disbur_attach)
                            disburattach_db.mutil_insert_attachment(disbur_attach)
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

def disbursement_delete(request):
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
            disbur_db.multi_delete(id_list)
            # 删除附件
            disburattach_db. multi_delete_attach_by_edit_id(id_list)
            ret['status'] = True
    except Exception as e:
        print(e)
        ret['message'] = "删除失败"
    return HttpResponse(json.dumps(ret))

def disbursement_detail(request):
    id = request.GET.get("id", None)
    ret = {"status": False, "data": "", "message": ""}
    if id:
        try:
            disbur_obj = disbur_db.query_disbur_by_id(id)
            if disbur_obj:
                # 格式化数据
                disbur_json = disbur_obj.__dict__
                disbur_json.pop('_state')
                disbur_json["company_id"] = change_to_company(disbur_json["company_id"])
                disbur_json["project_id"] = change_to_project(disbur_json["project_id"])
                disbur_json["classify_id"] = change_to_incomeclassify(disbur_json["classify_id"])
                disbur_json["associates_id"] = change_to_associates(disbur_json["associates_id"])
                disbur_json["approver_id"] = change_to_approver2(disbur_json["approver_id"])
                disbur_attach = disburattach_db.query_disbur_attachment(id)
                if disbur_attach:
                    disbur_json['attach'] = serializers.serialize("json", disbur_attach)
                else:
                    disbur_json['attach'] = ''
                ret['status'] = True
                ret['data'] = disbur_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request, '404.html')

def income_classify(request):
    query_sets = incomeclassify_db.query_classify_list()
    return render(request, "revenue/income_classify_list.html", {"query_sets": query_sets})

def income_classify_edit(request):
    """"收入分类添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            classify_obj = incomeclassify_db.query_classify_by_id(id)
        else:
            id = 0
            classify_obj = []
        return render(request, 'revenue/income_classify_edit.html',
                      {"classify_obj": classify_obj, "id": id})
    else:
        form = IncomeClassifyForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", "")
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = incomeclassify_db.query_classify_by_id(id)
                    final_info = compare_fields(Income_classify._update, record, data)
                    if final_info:
                        final_info["id"] = id
                        incomeclassify_db.update_classify_title(final_info)
                    ret['status'] = True
                    ret["data"] = id
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    incomeclassify_db.insert_classify_title(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))

def income_classify_delete(request):
    """分类删除"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        incomeclassify_db.multi_delete(id_list)
        ret['status'] = True
    except Exception as e:
        print(e)
        ret['status'] = "删除失败"
    return HttpResponse(json.dumps(ret))

def income_staff(request):
    """根据部门获取员工"""
    ret = {"status": False, "data": '', "message": ''}
    dpid = request.GET.get("dpid", None)
    if dpid:
        try:
            if int(dpid) == 0:
                dp_staff_list = approver2_db.query_approver2_list()
            else:
                dp_staff_list = approver2_db.query_approver2_by_department_id(dpid)
            # 序列化queryset对象
            dp_staff_list = serializers.serialize("json", dp_staff_list)
            ret['status'] = True
            ret["data"] = dp_staff_list
        except Exception as e:
            ret["message"] = "出错了"
    else:
        ret["message"] = "请选择相应的部门"
    return HttpResponse(json.dumps(ret))

