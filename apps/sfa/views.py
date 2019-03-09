import json
import os
import sys
import traceback
import uuid
from django.shortcuts import render,HttpResponse
from django.core import serializers
from django.db import transaction
from .forms.form import *
from common.functions import *
from .server import *
from .templatetags.sfa_tags import *
from personnel.templatetags.personnel_tags import *
# Create your views here.
from .utils import build_customer_filter,is_valid_date
import logging
logger = logging.getLogger(__name__)


def customer_center(request):
    sort = int(request.GET.get("sort",0))
    sign = int(request.GET.get("sign",2))
    dpid = int(request.GET.get("dpid", 0))
    sid = int(request.GET.get("sid", 0))
    stime = is_valid_date(request.GET.get("stime", ''))
    etime = is_valid_date(request.GET.get("etime", ''))
    filter = build_customer_filter(sign, **{"sort":sort,"dpid":dpid,"sid":sid,"stime":stime,"etime":etime})
    query_sets = customer_db.query_customer_by_filter(filter)

    return render(request, 'sfa/customer_center.html', {"query_sets": query_sets,"sort":sort,"sign":sign,
                                                        "sid":sid,"dpid":dpid,"stime":stime,"etime":etime})


def customer(request):
    sort = int(request.GET.get("sort", 0))
    sign = int(request.GET.get("sign", 2))
    follower = request.user.staff.sid
    query_sets = customer_db.query_customer_by_follower(follower)
    if sort > 0:
        query_sets = query_sets.filter(purpose_id=sort).all()
    if sign < 2:
        query_sets = query_sets.filter(is_sign=sign).all()
    return render(request, 'sfa/customer.html', {"query_sets": query_sets,"sort":sort,"sign":sign})


def customer_public(request):
    sort = int(request.GET.get("sort", 0))
    sign = int(request.GET.get("sign", 2))
    follower = 0
    query_sets = customer_db.query_customer_by_follower(follower)
    if sort > 0:
        query_sets = query_sets.filter(purpose_id=sort).all()
    if sign < 2:
        query_sets = query_sets.filter(is_sign=sign).all()
    return render(request, 'sfa/customer_public.html', {"query_sets": query_sets,"sort":sort,"sign":sign})


def customer_edit(request):
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        if nid:
            # 更新
            query_sets = customer_db.query_customer_by_id(nid)
            customer_photo = customer_photo_db.query_customer_photo(nid)
            customer_licence = customer_licence_db.query_customer_licence(nid)
            customer_attach = customer_attach_db.query_customer_attachment(nid)
            if not customer_photo:
                customer_photo = ''
            if not customer_attach:
                customer_attach = ''
            if not customer_licence:
                customer_licence = ''
        else:
            query_sets = {}
            customer_photo = {}
            customer_licence = {}
            customer_attach = {}
        return render(request, "sfa/customer_edit.html", {"query_set": query_sets,
                                                             "customer_photo": customer_photo,
                                                             "customer_licence": customer_licence,
                                                             "customer_attach": customer_attach,
                                                             "nid": nid})
    else:
        ret = {'status': False, "data": '', "message": ""}
        form = CustomerForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            customer_photo = data.get("customer_photo", None)
            customer_licence = data.get("customer_licence", None)
            customer_attach = data.get("attach", None)
            nid = data.get("nid", None)
            customer_photo = json.loads(customer_photo)
            customer_licence = json.loads(customer_licence)
            customer_attach = list(json.loads(customer_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新客户信息
                        record = customer_db.query_customer_by_id(nid)
                        customer_info = compare_fields(CustomerInfo._update, record, data)
                        if customer_info:
                            customer_info["nid"] = nid
                        if not customer_info["employees"]:
                            customer_info["employees"] = 0
                        print("customer_info",customer_info)
                        customer_db.update_customer(customer_info)
                        # 插入客户照片
                        photo_record = customer_photo_db.query_customer_photo(nid)
                        if customer_photo:
                            # 数据对比
                            customer_photo["customer_id"] = nid
                            if photo_record:
                                final_photo = compare_fields(CustomerPhoto._update, photo_record, customer_photo)
                                final_photo["customer_id"] = nid
                                if final_photo:
                                    customer_photo_db.update_photo(final_photo)
                            else:
                                customer_photo_db.insert_photo(customer_photo)
                        else:
                            # 删除旧数据
                            if photo_record:
                                customer_photo_db.delete_photo_by_customer_id(nid)
                        # 插入供应商执照
                        licence_record = customer_licence_db.query_customer_licence(nid)
                        if customer_licence:
                            # 数据对比
                            customer_licence["customer_id"] = nid
                            if licence_record:
                                final_photo = compare_fields(CustomerLicence._update, licence_record, customer_licence)
                                final_photo["customer_id"] = nid
                                if final_photo:
                                    customer_licence_db.update_licence(final_photo)
                            else:
                                customer_licence_db.insert_photo(customer_licence)
                        else:
                            # 删除旧数据
                            if licence_record:
                                customer_licence_db.delete_licence_by_customer_id(nid)
                        # 更新附件
                        if customer_attach:
                            att_record = customer_attach_db.query_customer_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, customer_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"customer_id": nid}, insert_att)
                                customer_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                customer_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                customer_attach_db.mutil_delete_customer_attachment(delete_id_att)
                        else:
                            customer_attach_db.multi_delete_attach_by_customer_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    logger.info(str(e))
                    traceback.print_exc()
                    ret["message"] = "出错了"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入供应商信息
                        customer_info = filter_fields(CustomerInfo._insert, data)
                        # 默认D类客户
                        purpose_list = customer_purpose_db.query_purpose_list()
                        for item in purpose_list:
                            if item.content == "C类": # 获取D类客户id
                                purpose_id = item.nid  #
                            else:
                                purpose_id = 6
                        customer_info["purpose_id"] = purpose_id

                        is_exist = CustomerInfo.objects.filter(company=customer_info["company"], town_id=customer_info["town_id"]).select_related("follower").first()
                        if is_exist:
                            raise Exception("客户已存在,跟进人:{0}".format(is_exist.follower))
                        nid = customer_db.insert_customer(customer_info)
                        # 插入客户照片
                        if customer_photo:
                            customer_photo["customer_id"] = nid
                            customer_photo_db.insert_photo(customer_photo)
                        # 插入客户执照
                        if customer_licence:
                            customer_licence["customer_id"] = nid
                            customer_licence_db.insert_photo(customer_licence)
                        if customer_attach:
                            # 插入客户附件
                            customer_attach = build_attachment_info({"customer_id": nid}, customer_attach)
                            customer_attach_db.mutil_insert_attachment(customer_attach)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    pass
                    ret["message"] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def customer_delete(request):
    """删除客户信息"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        print("id_list",id_list)
        customer_db.multi_delete(id_list)
        ret['status'] = True
    except Exception as e:
        ret['message'] = "删除失败"
    return HttpResponse(json.dumps(ret))


def linkman_delete(request):
    """删除客户联系人信息"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        c_linkman_db.multi_delete(id_list)
        ret['status'] = True
    except Exception as e:
        ret['message'] = "删除失败"
    return HttpResponse(json.dumps(ret))


def follow_delete(request):
    """删除客户跟进记录"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        c_follow_db.multi_delete(id_list)
        ret['status'] = True
    except Exception as e:
        ret['message'] = "删除失败"
    return HttpResponse(json.dumps(ret))


def memo_delete(request):
    """删除客户信息"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        c_memo_db.multi_delete(id_list)
        ret['status'] = True
    except Exception as e:
        ret['message'] = "删除失败"
    return HttpResponse(json.dumps(ret))


def contact_delete(request):
    """删除客户跟进信息"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        c_contact_db.multi_delete(id_list)
        ret['status'] = True
    except Exception as e:
        ret['message'] = "删除失败"
    return HttpResponse(json.dumps(ret))


def customer_detail(request):
    cid = request.GET.get("id",None)
    if cid:
        query_sets = customer_db.query_customer_by_id(cid)
        if query_sets:
            customer_photo = customer_photo_db.query_customer_photo(cid)
            customer_licence = customer_licence_db.query_customer_licence(cid)
            customer_attach = customer_attach_db.query_customer_attachment(cid)
            if not customer_photo:
                customer_photo = ''
            if not customer_licence:
                customer_licence = ''
            if not customer_attach:
                customer_attach = ''
            return render(request,"sfa/customer_detail.html",{"query_set": query_sets,
                                                                 "customer_photo": customer_photo,
                                                                 "customer_licence": customer_licence,
                                                                 "customer_attach": customer_attach,
                                                                })
    return render(request,'404.html')


def customer_linkman(request):
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        cid = request.GET.get("cid",'')
        if cid:
            customer_obj = customer_db.query_customer_by_id(cid)
            if customer_obj:
                if nid:
                    # 更新
                    query_sets = c_linkman_db.query_linkman_by_id(nid)
                    linkman_photo = c_linkman_photo_db.query_linkman_photo(nid)
                    linkman_card = c_linkman_card_db.query_linkman_card(nid)
                    linkman_attach = c_linkman_attach_db.query_linkman_attachment(nid)
                    if not linkman_photo:
                        linkman_photo = ''
                    if not linkman_card:
                        linkman_card = ''
                    if not linkman_attach:
                        linkman_attach = ''
                else:
                    query_sets = {}
                    linkman_photo = {}
                    linkman_card = {}
                    linkman_attach = {}
                return render(request, "sfa/customer_linkman.html", {"query_set": query_sets,
                                                                            "linkman_photo": linkman_photo,
                                                                            "linkman_card": linkman_card,
                                                                            "linkman_attach": linkman_attach,
                                                                            "nid": nid,
                                                                            "customer_obj":customer_obj
                                                                           })
        return render(request,"404.html")
    else:
        ret = {'status': False, "data": '', "message": ""}
        form = LinkmanForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            linkman_photo = data.get("linkman_photo", None)
            linkman_card = data.get("linkman_card", None)
            linkman_attach = data.get("attach", None)
            nid = data.get("nid", None)
            linkman_photo = json.loads(linkman_photo)
            linkman_card = json.loads(linkman_card)
            linkman_attach = list(json.loads(linkman_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新联系人信息
                        record = c_linkman_db.query_linkman_by_id(nid)
                        linkman_info = compare_fields(CustomerLinkman._update, record, data)
                        if linkman_info:
                            linkman_info["nid"] = nid
                            c_linkman_db.update_linkman(linkman_info)
                        # 插入联系人照片
                        photo_record = c_linkman_photo_db.query_linkman_photo(nid)
                        if linkman_photo:
                            # 数据对比
                            linkman_photo["linkman_id"] = nid
                            if photo_record:
                                final_photo = compare_fields(CustomerLinkmanPhoto._update, photo_record, linkman_photo)
                                final_photo["linkman_id"] = nid
                                if final_photo:
                                    c_linkman_photo_db.update_photo(final_photo)
                            else:
                                c_linkman_photo_db.insert_photo(linkman_photo)
                        else:
                            # 删除旧数据
                            if photo_record:
                                c_linkman_photo_db.delete_photo_by_linkman_id(nid)
                        # 插入联系人名片
                        card_record = c_linkman_card_db.query_linkman_card(nid)
                        if linkman_card:
                            # 数据对比
                            linkman_card["linkman_id"] = nid
                            if card_record:
                                final_photo = compare_fields(CustomerLinkmanCard._update, card_record, linkman_card)
                                final_photo["linkman_id"] = nid
                                if final_photo:
                                    c_linkman_card_db.update_card(final_photo)
                            else:
                                c_linkman_card_db.insert_photo(linkman_card)
                        else:
                            # 删除旧数据
                            if card_record:
                                c_linkman_card_db.delete_card_by_card_id(nid)
                        # 更新附件
                        if linkman_attach:
                            att_record = c_linkman_attach_db.query_linkman_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, linkman_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"linkman_id": nid}, insert_att)
                                c_linkman_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                c_linkman_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                c_linkman_attach_db.mutil_delete_linkman_attachment(delete_id_att)
                        else:
                            c_linkman_attach_db.multi_delete_attach_by_linkman_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入供应商信息
                        linkman_info = filter_fields(CustomerLinkman._insert, data)
                        nid = c_linkman_db.insert_linkman(linkman_info)
                        # 插入联系人照片
                        if linkman_photo:
                            linkman_photo["linkman_id"] = nid
                            c_linkman_photo_db.insert_photo(linkman_photo)
                        # 插入联系人名片
                        if linkman_card:
                            linkman_card["linkman_id"] = nid
                            c_linkman_card_db.insert_photo(linkman_card)
                        if linkman_attach:
                            linkman_attach = build_attachment_info({"linkman_id": nid}, linkman_attach)
                            c_linkman_attach_db.mutil_insert_attachment(linkman_attach)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def c_linkman_detail(request):
    id = request.GET.get("id",None)
    ret={"status":False,"data":"","message":""}
    if id:
        try:
            linkman_obj = c_linkman_db.query_linkman_by_id(id)
            if linkman_obj:
                # 格式化数据
                linkman_json = linkman_obj.__dict__
                linkman_json.pop('_state')
                linkman_json["gender"] = change_to_gender(linkman_json["gender"])
                linkman_json['marriage'] = change_to_linkman_marriage(linkman_json['marriage'])
                linkman_json['job_title'] = change_to_job_title(linkman_json['job_title_id'])
                linkman_json['is_lunar'] = change_to_linkman_lunar(linkman_json['is_lunar'])
                linkman_photo = c_linkman_photo_db.query_linkman_photo(id)
                linkman_card = c_linkman_card_db.query_linkman_card(id)
                linkman_attach = c_linkman_attach_db.query_linkman_attachment(id)
                if linkman_photo:
                    linkman_json['photo'] = linkman_photo.photo
                else:
                    linkman_json['photo'] = ''
                if linkman_card:
                    linkman_json['card'] =linkman_card.photo
                else:
                    linkman_json['card'] = ''
                if linkman_attach:
                     linkman_json['attach'] = serializers.serialize("json",linkman_attach)
                else:
                    linkman_json['attach'] = ''
                ret['status']=True
                ret['data'] = linkman_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            pass
    return render(request,'404.html')


def c_folllow_detail(request):
    id = request.GET.get("id", None)
    ret = {"status": False, "data": "", "message": ""}
    if id:
        try:
            follow_obj = c_follow_db.query_follow_by_id(id)
            if follow_obj:
                # 格式化数据
                follow_json = follow_obj.__dict__
                follow_json.pop('_state')
                follow_json["way_id"] = change_to_follow_way(follow_json["way_id"])
                follow_json["contact_id"] = change_to_follow_contact(follow_json["contact_id"])
                follow_json['linkman_id'] = change_to_customer_linkman(follow_json['linkman_id'])
                follow_json['result_id'] = change_to_follow_result(follow_json['result_id'])
                follow_json['purpose_id'] = change_to_customer_purpose(follow_json['purpose_id'])
                follow_json['recorder_id'] = change_to_staff(follow_json['recorder_id'])
                follow_attach = c_follow_attach_db.query_follow_attachment(id)
                if follow_attach:
                    follow_json['attach'] = serializers.serialize("json", follow_attach)
                else:
                    follow_json['attach'] = ''
                ret['status'] = True
                ret['data'] = follow_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request, '404.html')


def c_contact_detail(request):
    """客户收支"""
    id = request.GET.get("id",None)
    ret={"status":False,"data":"","message":""}
    if id:
        try:
            contact_obj = c_contact_db.query_contact_by_id(id)
            if contact_obj:
                # 格式化数据
                contact_json = contact_obj.__dict__
                contact_json.pop('_state')
                contact_json["category"] = change_to_contact_category(contact_json["category"])
                contact_json['linkman_id'] = change_to_linkman(contact_json['linkman_id'])
                contact_attach = c_contact_attach_db.query_contact_attachment(id)
                if contact_attach:
                    contact_json['attach'] = serializers.serialize("json",contact_attach)
                else:
                    contact_json['attach'] = ''
                ret['status'] = True
                ret['data'] = contact_json
                return HttpResponse(json.dumps(ret,cls=CJSONEncoder))
        except Exception as e:
            pass
    return render(request,'404.html')


def customer_memo(request):
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        cid = request.GET.get("cid",'')
        if cid:
            customer_obj = customer_db.query_customer_by_id(cid)
            if customer_obj:
                if nid:
                    # 更新
                    query_sets = c_memo_db.query_memo_by_id(nid)
                    memo_attach = c_memo_attach_db.query_memo_attachment(nid)
                    if not memo_attach:
                        memo_attach = ''
                else:
                    query_sets = {}
                    memo_attach = {}
                return render(request, "sfa/customer_memo.html", {"query_set": query_sets,
                                                                            "memo_attach": memo_attach,
                                                                            "nid": nid,
                                                                            "customer_obj":customer_obj
                                                                           })
        return render(request,"404.html")
    else:
        ret = {'status': False, "data": '', "message": ""}
        form = MemoForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            memo_attach = data.get("attach", None)
            nid = data.get("nid", None)
            memo_attach = list(json.loads(memo_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新联系人信息
                        record = c_memo_db.query_memo_by_id(nid)
                        memo_info = compare_fields(CustomerMemo._update, record, data)
                        if memo_info:
                            memo_info["nid"] = nid
                            c_memo_db.update_memo(memo_info)
                        # 更新附件
                        if memo_attach:
                            att_record =c_memo_attach_db.query_memo_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, memo_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"memo_id": nid}, insert_att)
                                c_memo_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                c_memo_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                c_memo_attach_db.mutil_delete_memo_attachment(delete_id_att)
                        else:
                            c_memo_attach_db.multi_delete_attach_by_linkman_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    pass
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入备忘信息
                        memo_info = filter_fields(CustomerMemo._insert, data)
                        nid = c_memo_db.insert_memo(memo_info)
                        if memo_attach:
                            memo_attach = build_attachment_info({"memo_id": nid}, memo_attach)
                            c_memo_attach_db.mutil_insert_attachment(memo_attach)
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


def customer_contact(request):
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        sid = request.GET.get("sid",'')
        if sid:
            customer_obj = customer_db.query_customer_by_id(sid)
            if customer_obj:
                if nid:
                    # 更新
                    query_sets = c_contact_db.query_contact_by_id(nid)
                    contact_attach = c_contact_attach_db.query_contact_attachment(nid)
                    if not contact_attach:
                        contact_attach = ''
                else:
                    query_sets = {}
                    contact_attach = {}
                return render(request, "sfa/customer_contact.html", {"query_set": query_sets,
                                                                            "contact_attach": contact_attach,
                                                                            "nid": nid,
                                                                            "customer_obj":customer_obj
                                                                           })
        return render(request,"404.html")
    else:
        ret = {'status': False, "data": '', "message": ""}
        form = ContactForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            contact_attach = data.get("attach", None)
            nid = data.get("nid", None)
            contact_attach = list(json.loads(contact_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新联系人信息
                        record = c_contact_db.query_contact_by_id(nid)
                        contact_info = compare_fields(CustomerContact._update, record, data)
                        if contact_info:
                            contact_info["nid"] = nid
                            c_contact_db.update_contact(contact_info)
                        # 更新附件
                        if contact_attach:
                            att_record = c_contact_attach_db.query_contact_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, contact_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"contact_id": nid}, insert_att)
                                c_contact_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                c_contact_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                c_contact_attach_db.mutil_delete_linkman_attachment(delete_id_att)
                        else:
                            c_contact_attach_db.multi_delete_attach_by_linkman_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    pass
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入收支信息
                        contact_info = filter_fields(CustomerContact._insert, data)
                        nid = c_contact_db.insert_contact(contact_info)
                        if contact_attach:
                            contact_attach = build_attachment_info({"contact_id": nid}, contact_attach)
                            c_contact_attach_db.mutil_insert_attachment(contact_attach)
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


def c_memo_detail(request):
    id = request.GET.get("id",None)
    ret={"status":False,"data":"","message":""}
    if id:
        try:
            memo_obj = c_memo_db.query_memo_by_id(id)
            if memo_obj:
                # 格式化数据
                memo_json = memo_obj.__dict__
                memo_json.pop('_state')
                memo_json["recorder"]= change_to_staff(memo_json["recorder_id"])
                memo_attach = c_memo_attach_db.query_memo_attachment(id)
                if memo_attach:
                    memo_json['attach'] = serializers.serialize("json",memo_attach)
                else:
                    memo_json['attach'] = ''
                ret['status']=True
                ret['data'] = memo_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            pass
    return render(request,'404.html')


def customer_follow(request):
    """添加客户跟进记录"""
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", 0)
        cid = request.GET.get("cid",0)
        if cid:
            customer_obj = customer_db.query_customer_by_id(cid)
            if customer_obj:
                if nid:
                    # 更新
                    query_sets = c_follow_db.query_follow_by_id(nid)
                    follow_attach = c_follow_attach_db.query_follow_attachment(nid)
                    if not follow_attach:
                        follow_attach = ''
                else:
                    query_sets = {}
                    follow_attach = {}
                return render(request, "sfa/customer_follow.html", {"query_set": query_sets,
                                                                    "nid": nid,
                                                                     "attach": follow_attach,
                                                                     "customer_obj":customer_obj
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
                        record = c_follow_db.query_follow_by_id(nid)
                        follow_info = compare_fields(CustomerFollow._update, record, data)
                        if follow_info:
                            follow_info["nid"] = nid
                            c_follow_db.update_follow(follow_info)
                            # 更新客户意向
                            if follow_info.get("purpose_id", None):
                                modify = {"purpose_id":follow_info["purpose_id"],"nid": record.customer_id}
                                customer_db.update_customer(modify)
                            # 更新附件
                            if follow_attach:
                                att_record =c_follow_attach_db.query_follow_attachment(nid)
                                # 数据对比
                                insert_att, update_att, delete_id_att = compare_json(att_record, follow_attach, "nid")
                                if insert_att:
                                    insert_att = build_attachment_info({"follow_id": nid}, insert_att)
                                    c_follow_attach_db.mutil_insert_attachment(insert_att)
                                if update_att:
                                    c_follow_attach_db.mutil_update_attachment(update_att)
                                if delete_id_att:
                                    c_follow_attach_db.mutil_delete_follow_attachment(delete_id_att)
                            else:
                                c_follow_attach_db.multi_delete_attach_by_follow_id(nid)
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
                        follow_info = filter_fields(CustomerFollow._insert, data)
                        nid = c_follow_db.insert_follow(follow_info)
                        if follow_attach:
                            follow_attach = build_attachment_info({"follow_id": nid}, follow_attach)
                            c_follow_attach_db.mutil_insert_attachment(follow_attach)
                        # 更新客户意向分类
                        customer_info = CustomerInfo.objects.filter(nid=data["customer_id"]).update(purpose=data["purpose_id"])
                        print(customer_info)
                        print("customer_info",customer_info)
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


def follow_customer(request):
    """跟进客户"""
    ret = {'status': False, "data": "", "message": ""}
    user = request.user.staff.sid
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        modify_info = {"follower_id":user}
        customer_db.multi_follow(id_list,modify_info)
        ret['status'] = True
    except Exception as e:
        ret['status'] = "跟进失败"
    return HttpResponse(json.dumps(ret))


def customer_assign(request):
    """分配客户"""
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
            customer_db.multi_follow(id_list,modify_info)
            ret['status'] = True
        except Exception as e:
            ret['status'] = "分配失败"
    return HttpResponse(json.dumps(ret))


def abandon_customer(request):
    """放弃客户"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    id_list = tuple(id_list)
    try:
        from django.db import connection, connections
        cursor = connection.cursor()  # cursor = connections['default'].cursor()
        cursor.execute("""update customer_info SET follower_id = 0 where nid in %s""",[id_list,])
        cursor.close()
        ret['status'] = True
    except Exception as e:
        pass
        ret['message'] = "操作失败"
    return HttpResponse(json.dumps(ret))


def sea_rule_list(request):
    query_sets = sea_rule_db.query_rule_last()
    return render(request,"sfa/sea_rul_list.html",{"query_sets":query_sets})


def sea_rule_edit(request):
    """"公海设置"""
    form = RuleForm(data=request.GET)
    ret = {'status': False, "data": '', "message": ""}
    if form.is_valid():
        rule = request.GET.get("rule", 15)
        if rule:
            try:
                sea_rule_db.insert_rule(rule)
                ret['status'] = True
            except Exception as e:
                ret['message'] = str(e)
    else:
        errors = form.errors.as_data().values()
        firsterror = str(list(errors)[0][0])
        ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def customer_photo(request):
    """客户照片上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/inventory/customer/photo"
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    try:
        # 获取文件对象
        file_obj = request.FILES.get("file")
        raw_name = file_obj.name
        postfix = raw_name.split(".")[-1]
        if file_obj:
            file_name = str(uuid.uuid4())+"."+postfix
            if not os.path.exists(os.path.dirname(target_path)):
                os.makedirs(target_path)
            file_path = os.path.join(target_path, file_name)
            # os.path.join()在Linux/macOS下会以斜杠（/）分隔路径，而在Windows下则会以反斜杠（\）分隔路径,
            # 故统一路径将'\'替换成'/'
            file_path = file_path.replace('\\',"/")
            with open(file_path, "wb") as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
            ret["status"] = True
            ret["data"]['path'] = file_path
            ret["data"]['name'] = raw_name
    except Exception as e:
        pass
        ret["summary"] = str(e)
    return HttpResponse(json.dumps(ret))


def customer_licence(request):
    """客户执照上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/inventory/customer/licence"
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    try:
        # 获取文件对象
        file_obj = request.FILES.get("file")
        raw_name = file_obj.name
        postfix = raw_name.split(".")[-1]
        if file_obj:
            file_name = str(uuid.uuid4())+"."+postfix
            if not os.path.exists(os.path.dirname(target_path)):
                os.makedirs(target_path)
            file_path = os.path.join(target_path, file_name)
            # os.path.join()在Linux/macOS下会以斜杠（/）分隔路径，而在Windows下则会以反斜杠（\）分隔路径,
            # 故统一路径将'\'替换成'/'
            file_path = file_path.replace('\\',"/")
            with open(file_path, "wb") as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
            ret["status"] = True
            ret["data"]['path'] = file_path
            ret["data"]['name'] = raw_name
    except Exception as e:
        pass
        ret["summary"] = str(e)
    return HttpResponse(json.dumps(ret))


def customer_attach(request):
    """客户附件上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/inventory/customer/attach"
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