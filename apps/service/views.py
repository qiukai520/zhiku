import json
from django.shortcuts import render, HttpResponse
from django.db import transaction
from contract.server import contract_db
from .server import *
from common.functions import filter_fields,compare_fields,compare_json,build_attachment_info
from .forms.form import FollowForm

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