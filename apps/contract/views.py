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
from .forms.form import ProductForm, MealForm, ContractForm

# Create your views here.


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
                    ret['message'] = str(e)
            else:
                try:
                    product_db.insert_product(data)
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
                    print(e)
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
                    print(e)
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
    is_approved = int(request.GET.get("is_approved",2))
    query_sets = contract_db.query_contract_list()
    if is_approved < 3:
        query_sets = query_sets.filter(is_approved=is_approved)
    return render(request, "contract/contract_list.html", {"query_sets": query_sets})


def customer_contract(request):
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        sid = request.GET.get("sid",'')
        if sid:
            customer_obj = customer_db.query_customer_by_id(sid)
            if customer_obj:
                if nid:
                    # 更新
                    query_sets = contract_db.query_contract_by_id(nid)
                    contract_attach = contract_attach_db.query_contract_attachment(nid)
                    if not contract_attach:
                        contract_attach = ''
                else:
                    query_sets = {}
                    contract_attach = {}
                return render(request, "contract/contract_edit.html", {"query_set": query_sets,
                                                                            "contract_attach": contract_attach,
                                                                            "nid": nid,
                                                                            "customer_obj":customer_obj
                                                                           })
        return render(request,"404.html")
    else:
        ret = {'status': False, "data": '', "message": ""}
        form = ContractForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            contract_attach = data.get("attach", None)
            nid = data.get("nid", None)
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
                                contract_attach_db.mutil_delete_linkman_attachment(delete_id_att)
                        else:
                            contract_attach_db.multi_delete_attach_by_linkman_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    pass
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


def contract_attach(request):
    """合同上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/contract/attach"
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