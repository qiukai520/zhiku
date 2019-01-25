import json
import os
import uuid
from django.core import serializers
from django.db import transaction
from django.shortcuts import render, HttpResponse
from contract.server import *
from contract.models import Product,ProductMeal
from common.functions import *
from sfa.server import customer_db
from .forms.form import ProductForm, MealForm, ContractForm,PaymentForm,LocationForm
import logging
# Create your views here.
logger = logging.getLogger(__name__)


def product_list(request):
    query_sets = product_db.query_product_list()
    return render(request,"contract/product_list.html",{"query_sets":query_sets})


def product_edit(request):
    """"产品添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            product_obj = product_db.query_product_by_id(id)
        else:
            id = 0
            product_obj = []
        return render(request, 'contract/product_edit.html', {"product_obj": product_obj, "id": id})
    else:
        form = ProductForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", 0)
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = product_db.query_product_by_id(id)
                    final_info = compare_fields(Product._update,record,data)
                    if final_info:
                        final_info["id"] = id
                        product_db.update_product(final_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    logger.error(e)
                    ret['message'] = "更新失败"
            else:
                try:
                    product_db.insert_product(data)
                    ret['status'] = True
                except Exception as e:
                    logger.error(e)
                    ret['message'] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def location_list(request):
    query_sets = c_location_db.query_location_list()
    return render(request,"contract/location_list.html",{"query_sets":query_sets})


def location_edit(request):
    """"坐标添加,编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            location_obj = c_location_db.query_location_by_id(id)
        else:
            id = 0
            location_obj = []
        return render(request, 'contract/location_edit.html', {"location_obj": location_obj, "id": id})
    else:
        form = LocationForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", 0)
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = c_location_db.query_location_by_id(id)
                    final_info = compare_fields(ContractLocation._update,record,data)
                    if final_info:
                        final_info["id"] = id
                        c_location_db.update_location(final_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    logger.error(e)
                    ret['message'] = "更新失败"
            else:
                try:
                    c_location_db.insert_location(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))



def meals(request):
    query_sets = product_meal_db.query_meal_list()
    return render(request, "contract/meal_list.html", {"query_sets": query_sets})


def meal_edit(request):
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        pid = request.GET.get("pid","")
        if pid:
            product_obj = product_db.query_product_by_id(pid)
            if product_obj:
                if nid:
                    # 更新
                    query_sets = product_meal_db.query_meal_by_id(nid)
                else:
                    query_sets = {}
                return render(request, "contract/product_meal_edit.html", {"query_set": query_sets,
                                                                            "nid": nid,
                                                                            "product_obj": product_obj
                                                                           })
        return render(request,"404.html")
    else:
        ret = {'status': False, "data": '', "message": ""}
        form = MealForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            nid = data.get("nid", None)
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新产品套餐信息
                        record = product_meal_db.query_meal_by_id(nid)
                        meal_info = compare_fields(ProductMeal._update,record, data)
                        if meal_info:
                            meal_info["nid"] = nid
                            product_meal_db.update_meal(meal_info)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    logger.error(e)
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入套餐信息
                        meal_info = filter_fields(ProductMeal._insert, data)
                        nid = product_meal_db.insert_meal(meal_info)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    logger.error(e)
                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def meals_delete(request):
    """删除产品套餐"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        product_meal_db.multi_delete(id_list)
        ret['status'] = True
    except Exception as e:
        ret['message'] = "删除失败"
    return HttpResponse(json.dumps(ret))


def fetch_meal(request):
    """根据产品获取相应的套餐"""
    ret = {"status":False,"data":"","message":""}
    id = request.GET.get("id")
    if id:
        data = {}
        meal_list = product_meal_db.query_meal_by_id(id)
        data["price"] = meal_list.price
        data["year_limit"] = meal_list.year_limit
        ret['status'] = True
        ret["data"] = data
    else:
        ret['message'] = "请选择相应的产品"
    from common.functions import DecimalEncoder
    return HttpResponse(json.dumps(ret,cls=DecimalEncoder))


def contracts_list(request):
    """我的合同"""
    is_approved = int(request.GET.get("is_approved",3))
    query_sets = contract_db.query_contract_list()
    if is_approved < 3:
        query_sets = query_sets.filter(is_approved=is_approved)
    return render(request, "contract/my_contracts.html", {"query_sets": query_sets, "is_approved":is_approved})


def add_payment(request):
    """尾款收付"""
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        cid = request.GET.get("cid","")
        if cid:
            contract_obj = contract_db.query_contract_by_id(cid)
            if contract_obj:
                if nid:
                    # 更新
                    query_sets = payment_db.query_payment_by_id(nid)
                    payment_attach = p_attach_db.query_payment_attachment(nid)
                    if not payment_attach:
                        payment_attach = ''
                else:
                    query_sets = {}
                    payment_attach = {}
                return render(request, "contract/payment.html", {"query_set": query_sets,
                                                                            "payment_attach": payment_attach,
                                                                            "nid": nid,
                                                                            "contract_obj":contract_obj
                                                                           })
        return render(request,"404.html")
    else:
        ret = {'status': False, "data": '', "message": ""}
        form = PaymentForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            payment_attach = data.get("attach", '')
            nid = data.get("nid", None)
            payment_attach = list(json.loads(payment_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新尾款信息
                        record = payment_db.query_payment_by_id(nid)
                        payment_info = compare_fields(ContractPayment._update, record, data)
                        if payment_info:
                            payment_info["nid"] = nid
                            payment_db.update_payment(payment_info)
                        # 更新附件
                        if payment_attach:
                            # 更新附件
                            att_record = p_attach_db.query_payment_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, payment_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"payment_id": nid}, insert_att)
                                p_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                p_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                p_attach_db.mutil_delete_attachment(delete_id_att)
                        else:
                            p_attach_db.multi_delete_attach_by_payment_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    logger.error(e)
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入尾款信息
                        payment_info = filter_fields(ContractPayment._insert, data)
                        nid = payment_db.insert_payment(payment_info)
                        if payment_attach:
                            payment_attach = build_attachment_info({"payment_id": nid}, payment_attach)
                            p_attach_db.mutil_insert_attachment(payment_attach)
                            # 构造合同审核记录
                            approver_list = approver_db.query_approver_list()
                            if approver_list:
                                app_record = []
                                for item in approver_list:
                                    obj = {}
                                    obj["payment_id"] = nid
                                    obj["approver_id"] = item.approver_id
                                    obj["follow"] = item.follow
                                    obj["result"] = 0
                                    app_record.append(obj)
                                p_apr_db.mutil_insert(app_record)
                            else:
                                # 如果没有审核人，则自动通过审核
                                # 尾款通过审核
                                payment_obj = payment_db.query_payment_by_id(nid)
                                payment_obj.is_approved = 1
                                payment_obj.save()
                                # 合同减掉尾款
                                balance = payment_obj.payment
                                contract_obj = contract_db.query_contract_by_id(payment_obj.contract_id)
                                contract_obj.received += balance
                                contract_obj.pending -= balance
                                contract_obj.save()
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    logger.error(e)
                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def payment_detail(request):
    """尾款详细"""
    id = request.GET.get("id",None)
    ret={"status":False,"data":"","message":""}
    if id:
        try:
            payment_obj = payment_db.query_payment_by_id(id)
            if payment_obj:
                # 格式化数据
                payment_json = payment_obj.__dict__
                payment_json.pop('_state')
                payment_attach = p_attach_db.query_payment_attachment(id)
                if payment_attach:
                    payment_json['attach'] = serializers.serialize("json",payment_attach)
                else:
                    payment_json['attach'] = ''
                ret['status']=True
                ret['data'] = payment_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            logger.error(e)
    return render(request,'404.html')

def contracts_center(request):
    """合同中心"""
    product_id = int(request.GET.get("product_id", 0))
    is_approved = int(request.GET.get("is_approved",3))
    query_sets = contract_db.query_contract_list()
    if product_id:
        query_sets = query_sets.filter(product_id=product_id)
    if is_approved < 3:
        query_sets = query_sets.filter(is_approved=is_approved)
    return render(request, "contract/contract_center.html", {"query_sets": query_sets,
                                                             "product_id": product_id,
                                                             "is_approved": is_approved})

import logging

def contract_approve(request):
    """合同审核列表"""
    log = logging.getLogger()
    log.info("approve")
    is_approved = int(request.GET.get("is_approved", 3))
    query_sets = contract_db.query_contract_list()
    if is_approved < 3:
        query_sets = query_sets.filter(is_approved=is_approved)

    return render(request, "contract/crt_apr_list.html", {"query_sets": query_sets,
                                                          "is_approved": is_approved})


def customer_contract(request):
    """合同"""
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        cid = request.GET.get("sid",'')
        if nid:
            # 更新
            query_sets = contract_db.query_contract_by_id(nid)
            if query_sets:
                customer_obj = customer_db.query_customer_by_id(query_sets.customer_id)
                contract_attach = contract_attach_db.query_contract_attachment(nid)
                if not contract_attach:
                    contract_attach = ''

            else:
                return render(request, "404.html")
        else:
            if cid:
                customer_obj = customer_db.query_customer_by_id(cid)
            else:
                return render(request, "404.html")
            query_sets = {}
            contract_attach = {}
        return render(request, "contract/contract_edit.html", {"query_set": query_sets,
                                                                            "contract_attach": contract_attach,
                                                                            "nid": nid,
                                                                            "customer_obj":customer_obj
                                                                           })
    else:
        ret = {'status': False, "data": '', "message": ""}
        form = ContractForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            contract_attach = data.get("attach", None)
            nid = data.get("nid", None)
            logger.error("nid",nid)
            contract_attach = list(json.loads(contract_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新合同信息
                        record = contract_db.query_contract_by_id(nid)
                        contract_info = compare_fields(ContractInfo._update, record, data)
                        if contract_info:
                            contract_info["nid"] = nid
                            contract_db.update_contract(contract_info)
                        # 更新附件
                        if contract_attach:
                            att_record = contract_attach_db.query_contract_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, contract_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"contract_id": nid}, insert_att)
                                contract_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                contract_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                contract_attach_db.mutil_delete_attachment(delete_id_att)
                        else:
                            contract_attach_db.multi_delete_attach_by_contract_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入合同信息
                        contract_info = filter_fields(ContractInfo._insert, data)
                        nid = contract_db.insert_contract(contract_info)
                        if contract_attach:
                            contract_attach = build_attachment_info({"contract_id": nid}, contract_attach)
                            contract_attach_db.mutil_insert_attachment(contract_attach)
                        # 构造合同审核记录
                        approver_list=approver_db.query_approver_list()
                        if approver_list:
                            app_record = []
                            for item in approver_list:
                                obj = {}
                                obj["contract_id"] = nid
                                obj["approver_id"] = item.approver_id
                                obj["follow"] = item.follow
                                obj["result"] = 0
                                app_record.append(obj)
                            approver_result_db.mutil_insert(app_record)
                        else:
                            # 如果没有审核人，则自动通过审核
                            ContractInfo.objects.filter(nid=nid).update(**{"is_approved":1})
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:

                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def contract_detail(request):
    """合同详细"""
    nid = request.GET.get("id",None)
    if nid:
        query_sets = contract_db.query_contract_by_id(nid)
        if query_sets:
            contract_attach = contract_attach_db.query_contract_attachment(nid)
            if not contract_attach:
                contract_attach = ''
            return render(request,"contract/contract_detail.html",{"query_set": query_sets,
                                                                 "contract_attach": contract_attach,
                                                                })
    return render(request,'404.html')


def approve_record(request):
    """审核记录"""
    type_ = int(request.GET.get("type", 0))
    if type_ == 1:
        pid = request.GET.get("id", 0)
        if pid:
            # 尾款审核记录
            query_sets = payment_db.query_payment_by_id(pid)
            result_list = p_apr_db.query_result_by_payment(pid)
        else:
            query_sets = ''
            result_list = ''
    else:
        result_id = request.GET.get("id", 0)
        if result_id:
            # 合同审核记录
            result_list = approver_result_db.query_record_by_id(result_id)
            query_sets = contract_db.query_contract_by_id(result_list.first().contract_id)
        else:
            query_sets = ''
            result_list = ''
    return render(request,"contract/approve_record.html",{"query_sets": query_sets,"result_list":result_list,"type":type_ })


def approve_detail(request):
    """合同审核详细"""
    nid = request.GET.get("id",None)
    if nid:
        query_sets = contract_db.query_contract_by_id(nid)
        if query_sets:
            contract_attach = contract_attach_db.query_contract_attachment(nid)
            if not contract_attach:
                contract_attach = ''
            return render(request,"contract/approved_detail.html",{"query_set": query_sets,
                                                                 "contract_attach": contract_attach,
                                                                })
    return render(request,'404.html')


def product_meal(request):
    """根据产品获取相应的套餐"""
    ret = {"status":False,"data":"","message":""}
    id = request.GET.get("id")
    if id:
        meal_list = product_meal_db.query_meal_by_product(id)
        data = serializers.serialize("json", meal_list)
        ret['status'] = True
        ret["data"]= data
    else:
        ret['message'] = "请选择相应的产品"
    return HttpResponse(json.dumps(ret))


def approver_list(request):
    """合同审核人管理"""
    query_sets = approver_db.query_approver_list()
    return render(request,"contract/approver_list.html",{"query_sets":query_sets})


def approve(request):
    """合同、尾款审核"""
    # type为0合同审核，1为尾款审核
    method = request.method
    if method == "GET":
        nid = int(request.GET.get("id",0))
        type_ = int(request.GET.get("type",0))
        user = request.user.staff.sid
        if nid and user:
            if type_ == 0:
                # 合同审核
                result_obj = approver_result_db.query_my_approved_result(nid, user)
                query_sets = contract_db.query_contract_by_id(nid)
                contract_obj = query_sets
                if result_obj:
                    record_list = app_record_db.query_my_record(result_obj.nid)
                    if not record_list:
                        record_list = ''
                else:
                    record_list=''
            else:
                # 尾款审核
                result_obj = p_apr_db.query_my_approved_result(nid, user)
                query_sets = payment_db.query_payment_by_id(nid)
                contract_obj = contract_db.query_contract_by_id(query_sets.contract_id)
                if result_obj:
                    record_list = p_apr_rcd_db.query_my_record(result_obj.nid)
                    if not record_list:
                        record_list = ''
                else:
                    record_list = ''
            return render(request, "contract/approve.html", {
                    "query_sets": query_sets,"contract_obj":contract_obj, "record_list": record_list, "type": type_
                })
        return render(request,"404.html")
    else:
        ret = {"status":False,"data":"","message":""}
        user = request.user.staff.sid
        data = request.POST
        type_ = int(data.get("type",0))
        result2 = int(data.get("result2", 0))
        print("type","result",type_,result2)
        if type_ == 1:
            # 尾款审核
            pid = int(data.get("payment_id", 0))
            if user and pid:
                try:
                    with transaction.atomic():
                        final_info = filter_fields(PaymentApproveRecord._insert,data)
                        result_obj = p_apr_db.query_my_approved_result(pid,user)
                        print("result_obj",result_obj)
                        final_info["result_id"] = result_obj.nid
                        if result2 == 1:
                            # 通过审核
                            PaymentApprove.objects.filter(payment_id=pid, approver_id=user).update(**{"result":1})
                            p_apr_rcd_db.insert_record(final_info)
                            # 查询是否所有都通过审核
                            result_list = p_apr_db.query_result_by_payment(pid)
                            flag = True
                            for obj in result_list:
                                if obj.result != 1:
                                    flag = False
                            if flag:
                                # 尾款通过审核
                                payment_obj = payment_db.query_payment_by_id(pid)
                                payment_obj.is_approved = 1
                                payment_obj.save()
                                # 合同减掉尾款
                                balance = payment_obj.payment
                                contract_obj = contract_db.query_contract_by_id(payment_obj.contract_id)
                                contract_obj.received += balance
                                contract_obj.pending -= balance
                                contract_obj.save()
                            ret["status"] = True
                        elif result2 == 2:
                            # 驳回
                            PaymentApprove.objects.filter(payment_id=pid, approver_id=user).update(**{"result":2})
                            p_apr_rcd_db.insert_record(final_info)
                            ret["status"] = True
                except Exception as e:
                    logger.error(e)
        else:
            # 合同审核
            cid = int(data.get("contract_id", 0))
            if user and cid:
                try:
                    with transaction.atomic():
                        final_info = filter_fields(ApproverRecord._insert,data)
                        result_obj = approver_result_db.query_my_approved_result(cid,user)
                        print("result_obj",result_obj)
                        final_info["result_id"] = result_obj.nid
                        if result2 == 1:
                            # 通过审核
                            ApproverResult.objects.filter(contract_id=cid, approver_id=user).update(**{"result":1})
                            app_record_db.insert_record(final_info)
                            # 查询是否所有都通过审核
                            result_list = approver_result_db.query_record_by_contract(cid)
                            flag = True
                            for obj in result_list:
                                if obj.result != 1:
                                    flag = False
                            if flag:
                                # 合同通过审核
                                contract_obj = contract_db.query_contract_by_id(cid)
                                contract_obj.is_approved = 1
                                contract_obj.save()
                                # 客户更改为签约状态
                                customer_db.update_customer({"nid":contract_obj.customer_id,"is_sign":1})
                            ret["status"] = True
                        elif result2 == 2:
                            # 驳回
                            ApproverResult.objects.filter(contract_id=cid, approver_id=user).update(**{"result":2})
                            app_record_db.insert_record(final_info)
                            ret["status"] = True
                except Exception as e:
                    logger.error(e)
        return HttpResponse(json.dumps(ret))


def approver_edit(request):
    """审核人编辑"""
    method = request.method
    if method == "GET":
        approver_list = approver_db.query_approver_list()
        return render(request, "contract/approver_edit.html", {"approver_list": approver_list})
    else:
        ret = {'status':False,"data":"","message":""}
        reviewers = request.POST.get("reviewers",None)
        if reviewers:
            try:
                with transaction.atomic():
                    reviewers = list(json.loads(reviewers))
                    record = approver_db.query_approver_list()
                    _, update_create_list, delete_id_list = compare_json(record,reviewers,"approver_id")
                    approver_db.mutil_update(reviewers)
                    approver_db.mutil_delete(delete_id_list)
                    ret["status"]= True
            except Exception as e:
                logger.error(e)
                ret["message"] = "更新失败"
        else:
            ret["message"] = "审核人不能为空"
        return HttpResponse(json.dumps(ret))


def contract_attach(request):
    """合同上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/contract/attach"
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
        logger.error(e)
        ret["summary"] = "上传失败"
    return HttpResponse(json.dumps(ret))