import json
import os
import sys
import traceback
import uuid
from django.shortcuts import render,HttpResponse,Http404
from django.db import transaction
from .forms.form import *
from common.functions import *
from .server import *
# Create your views here.


def customer_list(request):
    query_sets = customer_db.query_list()
    return render(request, 'sfa/customer_list.html', {"query_sets": query_sets})


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
                        # 更新商品信息
                        record = customer_db.query_customer_by_id(nid)
                        customer_info = compare_fields(CustomerInfo._update, record, data)
                        if customer_info:
                            customer_info["nid"] = nid
                            customer_db.update_customer(customer_info)
                        # 插入供应商照片
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
                    print(e)
                    ret["message"] = "出错了"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入供应商信息
                        customer_info = filter_fields(CustomerInfo._insert, data)

                        nid = customer_db.insert_customer(customer_info)
                        print("id",nid)
                        # 插入客户照片
                        if customer_photo:
                            customer_photo["customer_id"] = nid
                            customer_photo_db.insert_photo(customer_photo)
                        print("customer_photo",customer_photo)
                        # 插入客户执照
                        if customer_licence:
                            customer_licence["customer_id"] = nid
                            customer_licence_db.insert_photo(customer_licence)
                        if customer_attach:
                            # 插入客户附件
                            customer_attach = build_attachment_info({"customer_id": nid}, customer_attach)
                            customer_attach_db.mutil_insert_attachment(customer_attach)
                        print("customer_attach", customer_attach)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    ret["message"]="出错了"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def customer_photo(request):
    """供应商照片上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/inventory/customer/photo"
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
        print(e)
        ret["summary"] = str(e)
    return HttpResponse(json.dumps(ret))


def customer_licence(request):
    """供应商执照上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/inventory/customer/licence"
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
        print(e)
        ret["summary"] = str(e)
    return HttpResponse(json.dumps(ret))


def customer_attach(request):
    """商品附件上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/inventory/customer/attach"
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