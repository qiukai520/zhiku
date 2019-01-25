import json
from django.shortcuts import render, HttpResponse
from django.db import transaction
from django.core import serializers
from contract.server import contract_db
from .server import *
from common.functions import filter_fields,compare_fields,compare_json,build_attachment_info,CJSONEncoder
from .forms.form import FollowForm,WayForm,ContactForm
from contract.templatetags.contract_tags import change_to_customer_linkman, change_to_staff,\
    change_contract_follow_contact,change_contract_follow_way
from django.views import View

# Create your views here.


def service_assign(request):
    """分配客服"""
    ret = {'status': False, "data": "", "message": ""}
    sid = request.GET.get("sid", 0)
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    if sid:
        for item in ids:
            if item:
                id_list.append(int(item))
        try:
            modify_info = {"follower_id":sid}
            contract_db.multi_follow(id_list,modify_info)
            ret['status'] = True
        except Exception as e:
            pass
            ret['status'] = "分配失败"
    return HttpResponse(json.dumps(ret))


def my_assign(request):
    """我的客户"""
    user = request.user.staff.sid
    product_id = int(request.GET.get("product_id", 0))
    is_approved = int(request.GET.get("is_approved", 3))
    query_sets = contract_db.query_contract_by_follower(user)
    if product_id:
        query_sets = query_sets.filter(product_id=product_id)
    if is_approved < 3:
        query_sets = query_sets.filter(is_approved=is_approved)
    return render(request,"service/service_contract.html",{"query_sets":query_sets,"product_id":product_id,"is_approved":is_approved})


def contract_follow(request):
    """添加合同跟进记录"""
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", 0)
        cid = request.GET.get("cid",0)
        if cid:
            contract_obj = contract_db.query_contract_by_id(cid)
            if contract_obj:
                if nid:
                    # 更新
                    query_sets = crt_follow_db.query_follow_by_id(nid)
                    follow_attach = crt_follow_attach_db.query_follow_attachment(nid)
                    if not follow_attach:
                        follow_attach = ''
                else:
                    query_sets = {}
                    follow_attach = {}
                return render(request, "service/contract_follow.html", {"query_set": query_sets,
                                                                         "nid": nid,
                                                                         "attach": follow_attach,
                                                                         "contract_obj":contract_obj,
                                                                           })
        return render(request,"404.html")
    else:
        ret = {'status': False, "data": '', "message": ""}
        form = FollowForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            nid = data.get("nid", None)
            memo_attach = data.get("attach", None)
            follow_attach = list(json.loads(memo_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新联系人信息
                        record = crt_follow_db.query_follow_by_id(nid)
                        follow_info = compare_fields(ContractFollow._update, record, data)
                        if follow_info:
                            follow_info["nid"] = nid
                            crt_follow_db.update_follow(follow_info)
                            # 更新附件
                            if follow_attach:
                                att_record = crt_follow_attach_db.query_follow_attachment(nid)
                                # 数据对比
                                insert_att, update_att, delete_id_att = compare_json(att_record, follow_attach, "nid")
                                if insert_att:
                                    insert_att = build_attachment_info({"follow_id": nid}, insert_att)
                                    crt_follow_attach_db.mutil_insert_attachment(insert_att)
                                if update_att:
                                    crt_follow_attach_db.mutil_update_attachment(update_att)
                                if delete_id_att:
                                    crt_follow_attach_db.mutil_delete_follow_attachment(delete_id_att)
                            else:
                                crt_follow_attach_db.multi_delete_attach_by_follow_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入跟踪记录信息
                        follow_info = filter_fields(ContractFollow._insert, data)
                        nid = crt_follow_db.insert_follow(follow_info)
                        if follow_attach:
                            follow_attach = build_attachment_info({"follow_id": nid}, follow_attach)
                            crt_follow_attach_db.mutil_insert_attachment(follow_attach)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    pass
                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def follow_detail(request):
    id = request.GET.get("id", None)
    ret = {"status": False, "data": "", "message": ""}
    if id:
        try:
            follow_obj = ContractFollow.objects.filter(nid=id).select_related("way").first()
            if follow_obj:
                # 格式化数据
                data = {}
                follow_json = follow_obj.__dict__
                # follow_json.pop('_state')
                data["way_id"] = change_contract_follow_way(follow_json['way_id'])
                data["contact_id"] = change_contract_follow_contact(follow_json['contact_id'])
                data['linkman_id'] = change_to_customer_linkman(follow_json['linkman_id'])
                data['recorder_id'] = change_to_staff(follow_json['recorder_id'])
                data["detail"] = follow_json["detail"]
                data["next_step"] = follow_json["next_step"]
                data["date"] = follow_json["date"]
                follow_attach = crt_follow_attach_db.query_follow_attachment(id)
                if follow_attach:
                    data['attach'] = serializers.serialize("json", follow_attach)
                else:
                    data['attach'] = ''
                ret['status'] = True
                ret['data'] = data
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request, '404.html')


def way_list(request):
    """合同跟进方式"""
    query_sets = way_db.query_way_list()
    return render(request,"service/follow_way_list.html",{"query_sets":query_sets})


def way_edit(request):
    """"合同跟进方式添加/编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            way_obj = way_db.query_way_by_id(id)
        else:
            id = 0
            way_obj = []
        return render(request, 'service/follow_way_edit.html', {"way_obj": way_obj, "id": id})
    else:
        form = WayForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", "")
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = way_db.query_way_by_id(id)
                    # 对比数据是否有修改
                    final_info = compare_fields(FollowWay._update,record,data)
                    if final_info:
                        final_info["id"] = id
                        way_db.update_way(final_info)
                    ret["data"] = id
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    way_db.insert_way(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def contact_list(request):
    """合同跟进方式"""
    query_sets = contact_db.query_contact_list()
    return render(request, "service/follow_contact_list.html", {"query_sets": query_sets})


def contact_edit(request):
    """"合同跟进方式添加/编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            contact_obj = contact_db.query_contact_by_id(id)
        else:
            id = 0
            contact_obj = []
        return render(request, 'service/follow_contact_edit.html', {"contact_obj": contact_obj, "id": id})
    else:
        form = ContactForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", "")
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = contact_db.query_contact_by_id(id)
                    # 对比数据是否有修改
                    final_info = compare_fields(FollowContact._update, record, data)
                    if final_info:
                        final_info["id"] = id
                        contact_db.update_contact(final_info)
                    ret["data"] = id
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    contact_db.insert_contact(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def follow_delete(request):
    """删除合同跟进记录"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        crt_follow_db.multi_delete(id_list)
        ret['status'] = True
    except Exception as e:
        ret['message'] = "删除失败"
    return HttpResponse(json.dumps(ret))