import uuid
import os
from django.db import transaction
from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from django.core import serializers
from .server import *
from .forms.form import *
from common.functions import *
from .utils import *
from .templatetags.inventory_tags import *
from personnel.templatetags.personnel_tags import *
# Create your views here.



def goods_list(request):
    query_sets = goods_db.query_goods_list()
    return render(request, 'inventory/goods_list.html',{"query_sets":query_sets})

def search_goods(request):
    """商品查找"""
    ret = {'status': False, "data": '', "code": 200}
    code = request.GET.get("code",0)
    id = request.GET.get("id",0)
    data = {}
    if code:
        goods_obj = goods_db.query_goods_by_code(code)
    elif id:
        goods_obj = goods_db.query_goods_by_id(id)
    if goods_obj:
        data["goods_id"] = goods_obj.nid
        data["goods_name"] = goods_obj.name
        data["goods_unit"] = goods_obj.unit_id

        # 查询上一次的库存信息
        last_invent = invent_db.query_invent_by_goods(goods_obj.nid)
        if last_invent:
            data["warehouse_id"] = last_invent.warehouse_id
            data["location_id"] = last_invent.location_id
        else:
            data["warehouse_id"] = 0
            data["location_id"] = 0
        ret["status"] = True
    ret["data"] = data
    return HttpResponse(json.dumps(ret))


def goods_edit(request):
    """商品编辑"""
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        if nid:
            # 更新
            query_sets = goods_db.query_goods_by_id(nid)
            life_photo = goods_photo_db.query_goods_photo(nid)
            goods_code = goods_code_db.query_goods_bar(nid)
            goods_attach = goods_attach_db.query_goods_attachment(nid)
            if not life_photo:
                life_photo = {}
            if not goods_attach:
                goods_attach = {}
            if not goods_code:
                goods_code={}
        else:
            query_sets = {}
            life_photo = {}
            goods_attach = {}
            goods_code = {}
        return render(request, "inventory/goods_edit.html", {"query_set": query_sets,
                                                             "life_photo": life_photo,
                                                             "goods_code": goods_code,
                                                             "goods_attach": goods_attach,
                                                             "nid": nid})
    else:
        ret = {'status': False, "data": '', "message": ""}
        form = GoodsForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            goods_code = data.get("goods_code", '')
            goods_attach = data.get("attach", '')
            nid = data.get("nid", None)
            goods_code = json.loads(goods_code)
            goods_attach = list(json.loads(goods_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新商品信息
                        record = goods_db.query_goods_by_id(nid)
                        goods_info = compare_fields(Goods._update, record, data)
                        if goods_info:
                            goods_info["nid"] = nid
                            goods_db.update_goods(goods_info)
                        # 查看图片是否被修改
                        if "photo" in goods_info.keys():
                            # 删除服务器上的图片文件
                            modify_path_set = set(json.loads( goods_info.get("photo","[]")))
                            if record.photo:
                                record_photo_set = set(json.loads(record.photo))
                            else:
                                record_photo_set = set()
                            delete_path_set = record_photo_set - modify_path_set # 求差集（项在record中，但不在modify中）
                            for item in delete_path_set:
                                path = item[1:]
                                delete_server_file(path)
                        # 插入商品条码
                        code_record = goods_code_db.query_goods_bar(nid)
                        if goods_code:
                            # 数据对比
                            if code_record:
                                if code_record.photo != goods_code.get("photo",''):
                                    final_photo = goods_code
                                    final_photo["goods_id"]=nid
                                    goods_code_db.update_bar(final_photo)
                                    # 删除服务端上的文件
                                    code_path = code_record.photo
                                    delete_server_file(code_path)
                            else:
                                goods_code["goods_id"] = nid
                                goods_code_db.insert_bar(goods_code)
                        else:
                            # 删除旧数据
                            if code_record:
                                goods_code_db.delete_photo_by_goods_id(nid)
                                # 删除服务器上的文件
                                code_path = code_record.photo
                                delete_server_file(code_path)
                        # 更新附件
                        if goods_attach:
                            att_record = goods_attach_db.query_goods_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, goods_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"goods_id": nid}, insert_att)
                                goods_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                goods_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                goods_attach_db.mutil_delete_task_attachment(delete_id_att)
                        else:
                            goods_attach_db.multi_delete_attach_by_goods_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print(e)
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入商品信息
                        goods_info = filter_fields(Goods._insert, data)
                        nid = goods_db.insert_goods(goods_info)
                        # 插入商品条码照
                        if goods_code:
                            goods_code["goods_id"] = nid
                            goods_code_db.insert_bar(goods_code)
                        if goods_attach:
                            goods_attach = build_attachment_info({"goods_id": nid}, goods_attach)
                            goods_attach_db.mutil_insert_attachment(goods_attach)
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


def goods_detail(request):
    nid = request.GET.get("id",None)
    if nid:
        query_sets = goods_db.query_goods_by_id(nid)
        if query_sets:
            life_photo = goods_photo_db.query_goods_photo(nid)
            goods_code = goods_code_db.query_goods_bar(nid)
            goods_attach = goods_attach_db.query_goods_attachment(nid)
            if not life_photo:
                life_photo = ''
            if not goods_code:
                goods_code = ''
            if not goods_attach:
                goods_attach = ''
            return render(request,"inventory/goods_detail.html",{"query_set": query_sets,
                                                                 "life_photo": life_photo,
                                                                 "goods_code": goods_code,
                                                                 "goods_attach": goods_attach,
                                                                })
    return render(request,'404.html')

def goods_category_list(request):
    query_sets = goods_category_db.query_category_list()
    return render(request,"inventory/goods_category_list.html",{"query_sets":query_sets})


def goods_category_edit(request):
    """"供应商分类添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            obj = goods_category_db.query_category_by_id(id)
        else:
            id = 0
            obj = []
        return render(request, 'inventory/goods_category_edit.html', {"obj": obj, "id": id})
    else:
        form = GoodsCategoryForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", 0)
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = goods_category_db.query_category_by_id(id)
                    final_info = compare_fields(GoodsCategory._update,record,data)
                    if final_info:
                        final_info["nid"] = id
                        goods_category_db.update_category(final_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    goods_category_db.insert_category(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))





def goods_unit_list(request):
    query_sets = goods_unit_db.query_unit_list()
    return render(request,"inventory/goods_unit_list.html",{"query_sets":query_sets})


def goods_unit_edit(request):
    """"商品单位添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            obj = goods_unit_db.query_unit_by_id(id)
        else:
            id = 0
            obj = []
        return render(request, 'inventory/goods_unit_edit.html', {"obj": obj, "id": id})
    else:
        form = GoodsUnitForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", 0)
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = goods_unit_db.query_unit_by_id(id)
                    final_info = compare_fields(GoodsCategory._update,record,data)
                    if final_info:
                        final_info["nid"] = id
                        goods_unit_db.update_unit(final_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    goods_unit_db.insert_unit(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def industry_list(request):
    query_sets = industry_db.query_industry_list()
    return render(request,"inventory/industry_list.html",{"query_sets":query_sets})


def industry_edit(request):
    """"行业添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            obj = industry_db.query_industry_by_id(id)
        else:
            id = 0
            obj = []
        return render(request, 'inventory/industry_edit.html', {"obj": obj, "id": id})
    else:
        form = IndustryForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", 0)
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = industry_db.query_company_by_id(id)
                    final_info = compare_fields(Industry._update,record,data)
                    if final_info:
                        final_info["nid"] = id
                        industry_db.update_industry(final_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    industry_db.insert_industry(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def invent_list(request):
    """库存列表"""
    query_sets = goods_db.query_repertory_goods_list()
    return render(request,"inventory/invent_list.html",{"query_sets":query_sets})


class InventViewSet(View):
    """ 商品入库 """
    def get(self,request):
        id = request.GET.get("id", 0)
        gid = request.GET.get("gid","")
        # 有则为编辑 ,无则添加
        if gid:
            goods_obj = goods_db.query_goods_by_id(gid)
            if goods_obj:
                goods_obj={"nid":goods_obj.nid,"name":goods_obj.name}
                if id:
                    obj = invent_db.query_invent_by_id(id)
                    invent_attach = invent_attach_db.query_invent_attachment(id)
                    if obj:
                        obj = {"nid": obj.nid, "amount": obj.amount, "unit_id": obj.unit_id, "batch": obj.batch,"warehouse_id":obj.warehouse_id,
                               "location_id":obj.location_id,"date": obj.date,"recorder_id":obj.recorder_id}
                else:
                    id = 0
                    obj = {}
                    invent_attach = {}
                return render(request, "inventory/inventory_edit.html", {"obj": obj,"goods_obj":goods_obj,"invent_attach":invent_attach, "id": id})
        return render(request,"404.html")

    def post(self, request):
        form = InventForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("nid", 0)
            data = request.POST
            data = data.dict()
            invent_attach = data.get("attach", None)
            invent_attach = json.loads(invent_attach)
            # 有则为编辑 ,无则添加
            if id:
                try:
                    with transaction.atomic():
                        record = invent_db.query_invent_by_id(id)
                        final_info = compare_fields(Inventory._update, record, data)
                        final_info["nid"] = id
                        if final_info:
                            invent_db.invent_update(final_info)
                        if invent_attach:
                            att_record = invent_attach_db.query_invent_attachment(id)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, invent_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"inventory_id": id}, insert_att)
                                invent_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                invent_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                invent_attach_db.mutil_delete_invent_attachment(delete_id_att)
                        else:
                            invent_attach_db.delete_invent_attachment(id)
                        ret['status'] = True
                        ret['data'] = id
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
            else:
                try:
                    with transaction.atomic():
                        data_info = filter_fields(Inventory._insert, data)
                        last_record = invent_db.query_invent_by_goods_warehouse(data.get("goods_id",0),data.get("warehouse_id",0))
                        if last_record:
                            batch = last_record.batch + 1
                        else:
                            batch = 1
                        data_info["recorder_id"] = request.user.staff.sid
                        data_info["batch"] = batch
                        id = invent_db.insert_invent(data_info)
                        if invent_attach:
                            invent_attach = build_attachment_info({"inventory_id": id}, invent_attach)
                            invent_attach_db.mutil_insert_attachment(invent_attach)
                        ret['status'] = True
                        ret['data'] = id
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def invent_detail(request):
    """商品库存详细"""
    nid = request.GET.get("id",None)
    if nid:
        query_sets = goods_db.query_goods_by_id(nid)
        if query_sets:
            life_photo = goods_photo_db.query_goods_photo(nid)
            goods_code = goods_code_db.query_goods_bar(nid)
            goods_attach = goods_attach_db.query_goods_attachment(nid)
            if not life_photo:
                life_photo = ''
            if not goods_code:
                goods_code = ''
            if not goods_attach:
                goods_attach = ''
            return render(request,"inventory/invent_detail.html",{"query_set": query_sets,
                                                                 "life_photo": life_photo,
                                                                 "goods_code": goods_code,
                                                                 "goods_attach": goods_attach,
                                                                })
    return render(request,'404.html')


def invent_record(request):
    """入库记录详细"""
    id = request.GET.get("id",None)
    ret = {"status":False,"data":"","message":""}
    if id:
        try:
            invent_obj = invent_db.query_invent_by_id(id)
            if invent_obj:
                # 格式化数据
                invent_json = invent_obj.__dict__
                invent_json.pop('_state')
                invent_json["warehouse_id"] = change_to_warehouse(invent_json["warehouse_id"])
                invent_json['location_id'] = change_to_warelocation(invent_json['location_id'])
                invent_json['unit_id'] =change_to_goods_unit(invent_json['unit_id'])
                invent_json['recorder_id'] = change_to_staff(invent_json['recorder_id'])
                invent_attach = invent_attach_db.query_invent_attachment(id)
                if invent_attach:
                    invent_json['attach'] = serializers.serialize("json",invent_attach)
                else:
                    invent_json['attach'] = ''
                ret['status'] = True
                ret['data'] = invent_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request,'404.html')


class PurchaseViewSet(View):
    """采购录入"""
    def get(self,request):
        id = request.GET.get("id", "")
        gid = request.GET.get("gid","")
        # 有则为编辑 ,无则添加
        if gid:
            goods_obj = goods_db.query_goods_by_id(gid)
            if goods_obj:
                goods_obj={"nid":goods_obj.nid,"name":goods_obj.name}
                if id:
                    obj = purchase_db.query_purchase_by_id(id)
                    invent_attach = purchase_attach_db.query_purchase_attachment(id)
                    if obj:
                        obj = {"nid": obj.nid, "amount": obj.amount, "unit": obj.unit_id, "batch": obj.batch,
                               "supplier_id":obj.supplier_id, "linkman_id":obj.linkman_id,"date": obj.date,
                               "recorder_id":obj.recorder_id,"price":obj.price,"total_price":obj.total_price}
                else:
                    id = 0
                    obj = {}
                    invent_attach = {}
                return render(request, "inventory/purchase_edit.html", {"obj": obj,"goods_obj":goods_obj,"invent_attach":invent_attach, "id": id})
        return render(request,"404.html")

    def post(self, request):
        form = PurchaseForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("nid", 0)
            data = request.POST
            data = data.dict()
            purchase_attach = data.get("attach", None)
            purchase_attach = json.loads(purchase_attach)
            # 有则为编辑 ,无则添加
            if id:
                try:
                    with transaction.atomic():
                        record = purchase_db.query_purchase_by_id(id)
                        final_info = compare_fields(Purchase._update, record, data)
                        final_info["nid"] = id
                        if final_info:
                            purchase_db.purchase_update(final_info)
                            # 更新附件
                        if purchase_attach:
                            att_record = purchase_attach_db.query_purchase_attachment(id)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, purchase_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"purchase_id": id}, insert_att)
                                purchase_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                purchase_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                purchase_attach_db.mutil_delete_purchase_attachment(delete_id_att)
                        else:
                            print("delete",purchase_attach)
                            purchase_attach_db.delete_purchase_attachment(id)
                        ret['status'] = True
                        ret['data'] = id
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
            else:
                try:
                    with transaction.atomic():
                        data_info = filter_fields(Purchase._insert, data)
                        last_record = purchase_db.query_purchase_by_goods(data.get("goods_id",0))
                        if last_record:
                            batch = last_record.batch + 1
                        else:
                            batch = 1
                        data_info["recorder_id"] = request.user.staff.sid
                        data_info["batch"] = batch
                        id = purchase_db.insert_purchase(data_info)
                        if purchase_attach:
                            purchase_attach = build_attachment_info({"purchase_id": id}, purchase_attach)
                            purchase_attach_db.mutil_insert_attachment(purchase_attach)
                        ret['status'] = True
                        ret['data'] = id
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


class WastageViewSet(View):
    """损耗记录"""
    def get(self,request):
        id = request.GET.get("id", "")
        gid = request.GET.get("gid","")
        # 有则为编辑 ,无则添加
        if gid:
            goods_obj = goods_db.query_goods_by_id(gid)
            if goods_obj:
                goods_obj = {"nid":goods_obj.nid,"name":goods_obj.name,"unit_id":goods_obj.unit_id}
                if id:
                    obj = wastage_db.query_wastage_by_id(id)
                    wastage_attach = wastage_attach_db.query_wastage_attachment(id)
                    solver_objs =solver_db.query_wastage_solver(id)
                    solver_str=""
                    for item in solver_objs:
                       solver_str += str(item.sid_id)+","
                    if obj:
                        obj = {"nid": obj.nid, "amount": obj.amount, "unit": obj.unit_id,
                               "reason":obj.reason,"way":obj.way,"proposal": obj.proposal,
                               "goods_id":obj.goods_id,"date": obj.date,"recorder_id":obj.recorder_id}
                else:
                    id = 0
                    obj = {}
                    wastage_attach = {}
                    solver_str = ''
                return render(request, "inventory/wastage_edit.html", {"obj": obj,"goods_obj":goods_obj
                    ,"wastage_attach":wastage_attach,"solver_str":solver_str, "id": id})
        return render(request,"404.html")

    def post(self, request):
        form = WastageForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("nid", 0)
            data = request.POST
            data = data.dict()
            wastage_attach = data.get("attach", None)
            wastage_attach = json.loads(wastage_attach)
            # 获处理人
            solvers = data.get("solvers", None)
            solvers = list(json.loads(solvers))
            # 有则为编辑 ,无则添加
            if id:
                try:
                    print("edit",id)
                    with transaction.atomic():
                        record = wastage_db.query_wastage_by_id(id)
                        final_info = compare_fields(WastageGoods._update, record, data)
                        final_info["nid"] = id
                        if final_info:
                            wastage_db.wastage_update(final_info)
                            # 更新附件
                        if wastage_attach:
                            att_record = wastage_attach_db.query_wastage_attachment(id)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, wastage_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"wastage_id": id}, insert_att)
                                wastage_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                wastage_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                wastage_attach_db.mutil_delete_wastage_attachment(delete_id_att)
                        else:
                            wastage_attach_db.delete_wastage_attachment(id)
                        # 更新处理人
                        if solvers:
                            s_record = solver_db.query_wastage_solver(id)
                            modify_list = []
                            for item in solvers:
                                item["wid_id"] = id
                                modify_list.append(int(item.get("sid_id", 0)))
                            delete_list = []
                            for item in s_record:
                                if item.sid_id not in modify_list:
                                    delete_list.append(item.sid_id)
                            solver_db.mutil_delete(delete_list)
                            solver_db.mutil_insert(solvers)
                            # 待续
                        else:
                            solver_db.delete_wastage_solver(id)
                        ret['status'] = True
                        ret['data'] = id
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
            else:
                try:
                    with transaction.atomic():
                        data_info = filter_fields(WastageGoods._insert, data)
                        print("final_info",data_info)
                        id = wastage_db.insert_wastage(data_info)
                        if wastage_attach:
                            wastage_attach = build_attachment_info({"wastage_id": id}, wastage_attach)
                            wastage_attach_db.mutil_insert_attachment(wastage_attach)
                        if solvers:
                            solver_list = []
                            for item in solvers:
                                item["wid_id"] = id
                                solver_list.append(item)
                            print("solver_list",solver_list)
                            solver_db.mutil_insert(solver_list)

                        ret['status'] = True
                        ret['data'] = id
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def purchase_record(request):
    """采购记录详细"""
    id = request.GET.get("id",None)
    ret = {"status":False,"data":"","message":""}
    if id:
        try:
            purchase_obj = purchase_db.query_purchase_by_id(id)
            if purchase_obj:
                # 格式化数据
                purchase_json = purchase_obj.__dict__
                purchase_json.pop('_state')
                purchase_json["supplier_id"] = change_to_supplier(purchase_json["supplier_id"])
                purchase_json['linkman_id'] = change_to_linkman(purchase_json['linkman_id'])
                purchase_json['unit_id'] =change_to_goods_unit(purchase_json['unit_id'])
                purchase_json['recorder_id'] = change_to_staff(purchase_json['recorder_id'])
                purchase_attach = purchase_attach_db.query_purchase_attachment(id)
                if purchase_attach:
                    purchase_json['attach'] = serializers.serialize("json",purchase_attach)
                else:
                    purchase_json['attach'] = ''
                ret['status'] = True
                ret['data'] = purchase_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request,'404.html')


def wastage_detail(request):
    """入库记录详细"""
    id = request.GET.get("id",None)
    ret = {"status":False,"data":"","message":""}
    if id:
        try:
            wastage_obj = wastage_db.query_wastage_by_id(id)
            if wastage_obj:
                # 格式化数据
                wastage_json = wastage_obj.__dict__
                wastage_json.pop('_state')
                wastage_json['unit_id'] = change_to_goods_unit(wastage_json['unit_id'])
                wastage_json['recorder_id'] = change_to_staff(wastage_json['recorder_id'])
                wstage_attach = wastage_attach_db.query_wastage_attachment(id)
                solvers = fetch_wastage_solvers(id)
                wastage_json['solvers'] = solvers
                if wstage_attach:
                    wastage_json['attach'] = serializers.serialize("json",wstage_attach)
                else:
                    wastage_json['attach'] = ''
                ret['status'] = True
                ret['data'] = wastage_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request,'404.html')


def purchase_bind(request):
    pid = request.GET.get("pid",0)
    ids = request.GET.get("ids",'')
    ids = ids.split("|")
    ret = {"status": False, "data": "", "message": ""}
    if pid:
        # 转化成数字
        id_list = []
        for item in ids:
            if item:
                id_list.append(int(item))
        try:
            invent_db.mutil_update_purchase(id_list,pid)
            ret["status"]=True
        except Exception as e:
            print(e)
        return HttpResponse(json.dumps(ret))
    return render(request,"404.html")

def fetch_linkman(request):
    """根据供应商获取联系人"""
    ret = {"status":False,"data":"","message":""}
    id = request.GET.get("id")
    if id:
        linkman_list = linkman_db.query_linkman_by_supplier_id(id)
        # 序列化queryset对象
        data = serializers.serialize("json", linkman_list)
        ret['status'] = True
        ret["data"] = data
    else:
        ret['message'] = "请选择相应的供应商"
    return HttpResponse(json.dumps(ret))




def supplier_list(request):
    """供应商列表"""
    query_sets = supplier_db.query_supplier_list()
    return render(request, 'inventory/supplier_list.html', {"query_sets": query_sets})


def supplier_edit(request):
    """供应商编辑"""
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        if nid:
            # 更新
            query_sets = supplier_db.query_supplier_by_id(nid)
            supplier_photo = supplier_photo_db.query_supplier_photo(nid)
            supplier_licence = supplier_licence_db.query_supplier_licence(nid)
            supplier_attach = supplier_attach_db.query_supplier_attachment(nid)
            if not supplier_photo:
                supplier_photo = ''
            if not supplier_attach:
                supplier_attach = ''
            if not supplier_licence:
                supplier_licence = ''
        else:
            query_sets = {}
            supplier_photo = {}
            supplier_licence = {}
            supplier_attach = {}
        return render(request, "inventory/supplier_edit.html", {"query_set": query_sets,
                                                             "supplier_photo": supplier_photo,
                                                             "supplier_licence": supplier_licence,
                                                             "supplier_attach": supplier_attach,
                                                             "nid": nid})
    else:
        ret = {'status': False, "data": '', "message": ""}
        form = SupplierForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            supplier_photo = data.get("supplier_photo", None)
            supplier_licence = data.get("supplier_licence", None)
            supplier_attach = data.get("attach", None)
            nid = data.get("nid", None)
            supplier_photo = json.loads(supplier_photo)
            supplier_licence = json.loads(supplier_licence)
            supplier_attach = list(json.loads(supplier_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新商品信息
                        record = supplier_db.query_supplier_by_id(nid)
                        supplier_info = compare_fields(Supplier._update, record, data)
                        if supplier_info:
                            supplier_info["nid"] = nid
                            supplier_db.update_supplier(supplier_info)
                        # 插入供应商照片
                        photo_record = supplier_photo_db.query_supplier_photo(nid)
                        if supplier_photo:
                            # 数据对比
                            supplier_photo["supplier_id"] = nid
                            if photo_record:
                                final_photo = compare_fields(SupplierPhoto._update, photo_record, supplier_photo)
                                final_photo["supplier_id"] = nid
                                if final_photo:
                                    supplier_photo_db.update_photo(final_photo)
                            else:
                                supplier_photo_db.insert_photo(supplier_photo)
                        else:
                            # 删除旧数据
                            if photo_record:
                                supplier_photo_db.delete_photo_by_supplier_id(nid)
                        # 插入供应商执照
                        licence_record = supplier_licence_db.query_supplier_licence(nid)
                        if supplier_licence:
                            # 数据对比
                            supplier_licence["supplier_id"] = nid
                            if licence_record:
                                final_photo = compare_fields(SupplierLicence._update, licence_record, supplier_licence)
                                final_photo["supplier_id"] = nid
                                if final_photo:
                                    supplier_licence_db.update_licence(final_photo)
                            else:
                                supplier_licence_db.insert_photo(supplier_licence)
                        else:
                            # 删除旧数据
                            if licence_record:
                                supplier_licence_db.delete_licence_by_supplier_id(nid)
                        # 更新附件
                        if supplier_attach:
                            att_record = supplier_attach_db.query_supplier_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, supplier_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"supplier_id": nid}, insert_att)
                                supplier_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                supplier_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                supplier_attach_db.mutil_delete_supplier_attachment(delete_id_att)
                        else:
                            supplier_attach_db.multi_delete_attach_by_supplier_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入供应商信息
                        supplier_info = filter_fields(Supplier._insert, data)
                        nid = supplier_db.insert_supplier(supplier_info)
                        # 插入供应商照片
                        if supplier_photo:
                            supplier_photo["supplier_id"] = nid
                            supplier_photo_db.insert_photo(supplier_photo)
                        # 插入供应商执照
                        if supplier_licence:
                            supplier_licence["supplier_id"] = nid
                            supplier_licence_db.insert_photo(supplier_licence)
                        if supplier_attach:
                            supplier_attach = build_attachment_info({"supplier_id": nid}, supplier_attach)
                            supplier_attach_db.mutil_insert_attachment(supplier_attach)
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


def supplier_category_list(request):
    """供应商"""
    query_sets = supplier_category_db.query_category_list()
    return render(request,"inventory/supplier_category_list.html",{"query_sets":query_sets})


def supplier_category_edit(request):
    """"供应商分类"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            obj = supplier_category_db.query_category_by_id(id)
        else:
            id = 0
            obj = []
        return render(request, 'inventory/supplier_category_edit.html', {"obj": obj, "id": id})
    else:
        form = SupplierCategoryForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", 0)
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = supplier_category_db.query_category_by_id(id)
                    final_info = compare_fields(SupplierCategory._update,record,data)
                    if final_info:
                        final_info["nid"] = id
                        supplier_category_db.update_category(final_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    supplier_category_db.insert_category(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def retailers_list(request):
    """零售供应商"""
    query_sets = retailer_db.query_retail_list()
    return render(request,"inventory/retail_supplier_list.html",{"query_sets":query_sets})


def retailers_edit(request):
    """"零售供应商"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            obj = retailer_db.query_retail_by_id(id)
        else:
            id = 0
            obj = []
        return render(request, 'inventory/retail_supplier_edit.html', {"obj": obj, "id": id})
    else:
        form = RetailSupplierForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", 0)
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = retailer_db.query_retail_by_id(id)
                    final_info = compare_fields(RetailSupplier._update, record, data)
                    if final_info:
                        final_info["nid"] = id
                        retailer_db.update_retail(final_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    retailer_db.insert_retail(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def supplier_linkman(request):
    """供应商联系人"""
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        sid = request.GET.get("sid",'')
        if sid:
            supplier_obj = supplier_db.query_supplier_by_id(sid)
            if supplier_obj:
                if nid:
                    # 更新
                    query_sets = linkman_db.query_linkman_by_id(nid)
                    linkman_photo = linkman_photo_db.query_linkman_photo(nid)
                    linkman_card = linkman_card_db.query_linkman_card(nid)
                    linkman_attach = linkman_attach_db.query_linkman_attachment(nid)
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
                return render(request, "inventory/supplier_linkman.html", {"query_set": query_sets,
                                                                            "linkman_photo": linkman_photo,
                                                                            "linkman_card": linkman_card,
                                                                            "linkman_attach": linkman_attach,
                                                                            "nid": nid,
                                                                            "supplier_obj":supplier_obj
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
                        record = linkman_db.query_linkman_by_id(nid)
                        linkman_info = compare_fields(Linkman._update, record, data)
                        if linkman_info:
                            linkman_info["nid"] = nid
                            linkman_db.update_linkman(linkman_info)
                        # 插入联系人照片
                        photo_record = linkman_photo_db.query_linkman_photo(nid)
                        if linkman_photo:
                            # 数据对比
                            linkman_photo["linkman_id"] = nid
                            if photo_record:
                                final_photo = compare_fields(LinkmanPhoto._update, photo_record, linkman_photo)
                                final_photo["linkman_id"] = nid
                                if final_photo:
                                    linkman_photo_db.update_photo(final_photo)
                            else:
                                linkman_photo_db.insert_photo(linkman_photo)
                        else:
                            # 删除旧数据
                            if photo_record:
                                linkman_photo_db.delete_photo_by_linkman_id(nid)
                        # 插入联系人名片
                        card_record = linkman_card_db.query_linkman_card(nid)
                        if linkman_card:
                            # 数据对比
                            linkman_card["linkman_id"] = nid
                            if card_record:
                                final_photo = compare_fields(LinkmanCard._update, card_record, linkman_card)
                                final_photo["linkman_id"] = nid
                                if final_photo:
                                    linkman_card_db.update_card(final_photo)
                            else:
                                linkman_card_db.insert_photo(linkman_card)
                        else:
                            # 删除旧数据
                            if card_record:
                                linkman_card_db.delete_card_by_card_id(nid)
                        # 更新附件
                        if linkman_attach:
                            att_record = linkman_attach_db.query_linkman_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, linkman_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"linkman_id": nid}, insert_att)
                                linkman_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                linkman_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                linkman_attach_db.mutil_delete_linkman_attachment(delete_id_att)
                        else:
                            linkman_attach_db.multi_delete_attach_by_linkman_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入供应商信息
                        linkman_info = filter_fields(Linkman._insert, data)
                        nid = linkman_db.insert_linkman(linkman_info)
                        # 插入联系人照片
                        if linkman_photo:
                            linkman_photo["linkman_id"] = nid
                            linkman_photo_db.insert_photo(linkman_photo)
                        # 插入联系人名片
                        if linkman_card:
                            linkman_card["linkman_id"] = nid
                            linkman_card_db.insert_photo(linkman_card)
                        if linkman_attach:
                            linkman_attach = build_attachment_info({"linkman_id": nid}, linkman_attach)
                            linkman_attach_db.mutil_insert_attachment(linkman_attach)
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


def supplier_contact(request):
    """供应商来往"""
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        sid = request.GET.get("sid",'')
        if sid:
            supplier_obj = supplier_db.query_supplier_by_id(sid)
            if supplier_obj:
                if nid:
                    # 更新
                    query_sets = supplier_contact_db.query_contact_by_id(nid)
                    contact_attach = contact_attach_db.query_contact_attachment(nid)
                    if not contact_attach:
                        contact_attach = ''
                else:
                    query_sets = {}
                    contact_attach = {}
                return render(request, "inventory/supplier_contact.html", {"query_set": query_sets,
                                                                            "contact_attach": contact_attach,
                                                                            "nid": nid,
                                                                            "supplier_obj":supplier_obj
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
                        record = supplier_contact_db.query_contact_by_id(nid)
                        contact_info = compare_fields(SupplierContact._update, record, data)
                        if contact_info:
                            contact_info["nid"] = nid
                            supplier_contact_db.update_contact(contact_info)
                        # 更新附件
                        if contact_attach:
                            att_record = supplier_attach_db.query_supplier_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, contact_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"contact_id": nid}, insert_att)
                                contact_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                contact_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                contact_attach_db.mutil_delete_linkman_attachment(delete_id_att)
                        else:
                            contact_attach_db.multi_delete_attach_by_linkman_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入供应商信息
                        contact_info = filter_fields(SupplierContact._insert, data)
                        nid = supplier_contact_db.insert_contact(contact_info)
                        if contact_attach:
                            contact_attach = build_attachment_info({"contact_id": nid}, contact_attach)
                            contact_attach_db.mutil_insert_attachment(contact_attach)
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


def supplier_memo(request):
    """供应商备忘"""
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        sid = request.GET.get("sid",'')
        if sid:
            supplier_obj = supplier_db.query_supplier_by_id(sid)
            if supplier_obj:
                if nid:
                    # 更新
                    query_sets = supplier_memo_db.query_memo_by_id(nid)
                    memo_attach = memo_attach_db.query_memo_attachment(nid)
                    if not memo_attach:
                        memo_attach = ''
                else:
                    query_sets = {}
                    memo_attach = {}
                return render(request, "inventory/supplier_memo.html", {"query_set": query_sets,
                                                                            "memo_attach": memo_attach,
                                                                            "nid": nid,
                                                                            "supplier_obj":supplier_obj
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
                        record = supplier_memo_db.query_memo_by_id(nid)
                        memo_info = compare_fields(SupplierMemo._update, record, data)
                        if memo_info:
                            memo_info["nid"] = nid
                            supplier_memo_db.update_memo(memo_info)
                        # 更新附件
                        if memo_attach:
                            att_record = memo_attach_db.query_memo_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, memo_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"memo_id": nid}, insert_att)
                                memo_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                memo_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                memo_attach_db.mutil_delete_memo_attachment(delete_id_att)
                        else:
                            memo_attach_db.multi_delete_attach_by_linkman_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入备忘信息
                        memo_info = filter_fields(SupplierMemo._insert, data)
                        nid = supplier_memo_db.insert_memo(memo_info)
                        if memo_attach:
                            memo_attach = build_attachment_info({"memo_id": nid}, memo_attach)
                            memo_attach_db.mutil_insert_attachment(memo_attach)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def supplier_detail(request):
    """供应商详细"""
    sid = request.GET.get("id",None)
    if sid:
        query_sets = supplier_db.query_supplier_by_id(sid)
        if query_sets:
            supplier_photo = supplier_photo_db.query_supplier_photo(sid)
            supplier_licence = supplier_licence_db.query_supplier_licence(sid)
            supplier_attach = supplier_attach_db.query_supplier_attachment(sid)
            if not supplier_photo:
                supplier_photo = ''
            if not supplier_attach:
                supplier_attach = ''
            if not supplier_licence:
                supplier_licence = ''
            return render(request,"inventory/supplier_detail.html",{"query_set": query_sets,
                                                                 "supplier_photo": supplier_photo,
                                                                 "supplier_licence": supplier_licence,
                                                                 "supplier_attach": supplier_attach,
                                                                })
    return render(request,'404.html')


def contact_detail(request):
    """供应商联系人"""
    id = request.GET.get("id",None)
    ret={"status":False,"data":"","message":""}
    if id:
        try:
            contact_obj = supplier_contact_db.query_contact_by_id(id)
            if contact_obj:
                # 格式化数据
                contact_json = contact_obj.__dict__
                contact_json.pop('_state')
                contact_json["category"] = change_to_contact_category(contact_json["category"])
                contact_json['linkman_id'] = change_to_linkman(contact_json['linkman_id'])
                contact_attach = contact_attach_db.query_contact_attachment(id)
                if contact_attach:
                    contact_json['attach'] = serializers.serialize("json",contact_attach)
                else:
                    contact_json['attach'] = ''
                ret['status'] = True
                ret['data'] = contact_json
                print(ret)
                return HttpResponse(json.dumps(ret,cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request,'404.html')



def linkman_detail(request):
    id = request.GET.get("id",None)
    ret={"status":False,"data":"","message":""}
    if id:
        try:
            linkman_obj = linkman_db.query_linkman_by_id(id)
            if linkman_obj:
                # 格式化数据
                linkman_json = linkman_obj.__dict__
                linkman_json.pop('_state')
                linkman_json["gender"] = change_to_gender(linkman_json["gender"])
                linkman_json['marriage'] = change_to_linkman_marriage(linkman_json['marriage'])
                linkman_json["job_title"]= change_to_job_title(linkman_json["job_title_id"])
                linkman_json['is_lunar'] = change_to_linkman_lunar(linkman_json['is_lunar'])
                linkman_photo = linkman_photo_db.query_linkman_photo(id)
                linkman_card = linkman_card_db.query_linkman_card(id)
                linkman_attach = linkman_attach_db.query_linkman_attachment(id)
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
            print(e)
    return render(request,'404.html')


def price_detail(request):
    id = request.GET.get("id",None)
    ret={"status":False,"data":"","message":""}
    if id:
        try:
            price_obj = goods_price_db.query_price_by_id(id)
            if price_obj:
                # 格式化数据
                price_json = price_obj.__dict__
                price_json.pop('_state')
                price_json["supplier_id"] = change_to_supplier(price_json["supplier_id"])
                price_json['linkman_id'] = change_to_linkman(price_json['linkman_id'])
                price_json['unit_id'] =change_to_goods_unit(price_json['unit_id'])
                price_json['staff_id'] = change_to_staff(price_json['staff_id'])
                price_attach = price_attach_db.query_price_attachment(id)
                if price_attach:
                    price_json['attach'] = serializers.serialize("json",price_attach)
                else:
                    price_json['attach'] = ''
                ret['status']=True
                ret['data'] = price_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))

        except Exception as e:
            print(e)
    return render(request,'404.html')


def memo_detail(request):
    """备忘详细"""
    id = request.GET.get("id",None)
    ret={"status":False,"data":"","message":""}
    if id:
        try:
            memo_obj = supplier_memo_db.query_memo_by_id(id)
            if memo_obj:
                # 格式化数据
                memo_json = memo_obj.__dict__
                memo_json.pop('_state')
                memo_attach = memo_attach_db.query_memo_attachment(id)
                if memo_attach:
                    memo_json['attach'] = serializers.serialize("json",memo_attach)
                else:
                    memo_json['attach'] = ''
                ret['status']=True
                ret['data'] = memo_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request,'404.html')


def goods_delete(request):
    """商品软删除"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    status = {"delete_status": 0}
    try:
        goods_db.multi_delete(id_list, status)
        ret['status'] = True
    except Exception as e:
        print(e)
        ret['status'] = "删除失败"
    return HttpResponse(json.dumps(ret))


def add_repertory(request):
    """商品移入库存"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    print("ids",ids)
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        repertory_db.multi_insert(id_list)
        ret['status'] = True
    except Exception as e:
        print(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

def remove_repertory(request):
    """商品移出库存"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    print("ids",ids)
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        repertory_db.multi_delete(id_list)
        ret['status'] = True
    except Exception as e:
        ret['status'] = False
    return HttpResponse(json.dumps(ret))


def goods_price(request):
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        gid = request.GET.get("gid","")
        if gid:
            goods_obj = goods_db.query_goods_by_id(gid)
            if goods_obj:
                if nid:
                    # 更新
                    query_sets = goods_price_db.query_price_by_id(nid)
                    price_attach = price_attach_db.query_price_attachment(nid)
                    if not price_attach:
                        price_attach = ''
                else:
                    query_sets = {}
                    price_attach = {}
                return render(request, "inventory/goods_price.html", {"query_set": query_sets,
                                                                            "price_attach": price_attach,
                                                                            "nid": nid,
                                                                            "goods_obj":goods_obj
                                                                           })
        return render(request,"404.html")
    else:
        ret = {'status': False, "data": '', "message": ""}
        form = PriceForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            price_attach = data.get("attach", '')
            nid = data.get("nid", None)
            price_attach = list(json.loads(price_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新商品报价信息
                        record = goods_price_db.query_price_by_id(nid)
                        price_info = compare_fields(GoodsPrice._update, record, data)
                        if price_info:
                            price_info["nid"] = nid
                            goods_price_db.update_price(price_info)
                        # 更新附件
                        if price_attach:
                            # 更新附件
                            att_record = price_attach_db.query_price_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, price_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"price_id": nid}, insert_att)
                                price_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                price_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                price_attach_db.mutil_delete_price_attachment(delete_id_att)
                        else:
                            price_attach_db.multi_delete_attach_by_price_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入报价信息
                        price_info = filter_fields(GoodsPrice._insert, data)
                        print(price_info)
                        nid = goods_price_db.insert_price(price_info)
                        if price_attach:
                            price_attach = build_attachment_info({"price_id": nid}, price_attach)
                            price_attach_db.mutil_insert_attachment(price_attach)
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


def price_compare(request):
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        gid = request.GET.get("gid","")
        if gid:
            goods_obj = goods_db.query_goods_by_id(gid)
            if goods_obj:
                if nid:
                    # 更新
                    query_sets = price_compare_db.query_price_by_id(nid)
                else:
                    query_sets = {}
                return render(request, "inventory/goods_price_compare.html", {"query_set": query_sets,
                                                                            "nid": nid,
                                                                            "goods_obj":goods_obj
                                                                           })
        return render(request,"404.html")
    else:
        ret = {'status': False, "data": '', "message": ""}
        form = PriceCompareForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            nid = data.get("nid", None)
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新商品报价信息
                        record = price_compare_db.query_price_by_id(nid)
                        price_info = compare_fields(PriceCompare._update, record, data)
                        if price_info:
                            price_info["nid"] = nid
                            price_compare_db.update_price(price_info)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入报价信息
                        price_info = filter_fields(PriceCompare._insert, data)
                        print(price_info)
                        nid = price_compare_db.insert_price(price_info)
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


def supplier_delete(request):
    """供应商软删除"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    status = {"delete_status": 0}
    try:
        supplier_db.multi_delete(id_list, status)
        ret['status'] = True
    except Exception as e:
        print(e)
        ret['status'] = "删除失败"
    return HttpResponse(json.dumps(ret))


def warehouse_list(request):
    query_sets = warehouse_db.query_warehouse_list()
    return render(request,"inventory/warehouse_list.html",{"query_sets":query_sets})


class WarehouseViewSet(View):
    def get(self,request):
        id = request.GET.get("id", "")

        # 有则为编辑 ,无则添加
        if id:
            obj = warehouse_db.query_warehouse_by_id(id)
            if obj:
                obj ={"nid":obj.nid,"name":obj.name,"town_id":obj.town_id,"address":obj.address,"lng":obj.lng,"lat":obj.lat}
        else:
            id = 0
            obj = {}
        return render(request, "inventory/warehouse_edit.html",{"obj":obj,"id": id})

    def post(self, request):
        form = WarehouseForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", 0)
            data = request.POST
            data = data.dict()
            print("data",data)
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = warehouse_db.query_warehouse_by_id(id)
                    final_info = compare_fields(Warehouse._update, record, data)
                    print(final_info)
                    if final_info:
                        warehouse_db.update_warehouse(final_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
            else:
                try:
                    data_info = filter_fields(Warehouse._insert, data)
                    id = warehouse_db.insert_warehouse(data_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        print("ret",ret)
        return HttpResponse(json.dumps(ret))


def ware_location_list(request):
    query_sets = ware_location_db.query_location_list()
    return render(request,"inventory/ware_location_list.html",{"query_sets":query_sets})


class WareLocationViewSet(View):
    def get(self,request):
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            obj = ware_location_db.query_location_by_id(id)
            if obj:
                obj ={"nid":obj.nid,"name":obj.location,"warehouse":obj.warehouse_id}
        else:
            id = 0
            obj = {}
        return render(request, "inventory/ware_location_edit.html",{"obj":obj,"id": id})

    def post(self, request):
        form = WareLocationForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", 0)
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = ware_location_db.query_location_by_id(id)
                    final_info = filter_fields(WareLocation._update, data)
                    print(final_info)
                    if final_info:
                        final_info["nid"] = id
                        ware_location_db.update_location(final_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
            else:
                try:
                    data_info = filter_fields(WareLocation._insert, data)
                    ware_location_db.insert_location(data_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def warehouse_location(request):
    """根据仓库获取相应库位"""
    ret = {"status":False,"data":"","message":""}
    id =request.GET.get("id")
    if id:
        location_list =ware_location_db.query_location_by_house(id)
        # 序列化queryset对象
        data = serializers.serialize("json", location_list)
        ret['status'] = True
        ret["data"]= data
    else:
        ret['message'] = "请选择相应的仓库"

    return HttpResponse(json.dumps(ret))


def goods_photo(request):
    """商品照片上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/inventory/goods/photo"
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
        ret["summary"] = str(e)
    return HttpResponse(json.dumps(ret))


def webuploader_photo(request):
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    target_path = "media/upload/inventory/goods/"
    try:
        # 获取文件对象
        post_obj = request.POST
        file_obj = request.FILES.get("file")
        raw_name = file_obj.name
        raw_id = post_obj.get("id")
        postfix = raw_name.split(".")[-1]
        if file_obj:
            file_name = str(uuid.uuid4()) + "." + postfix
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
            ret["data"]["id"] = raw_id
    except Exception as e:
        ret["summary"] = str(e)
    return HttpResponse(json.dumps(ret))


def webuploader_photo_detele(request):
    ret = {"status": True, "data": {"path": "", "name": ""}, "summary": ""}
    return HttpResponse(json.dumps(ret))


def goods_code(request):
    """商品照片上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/inventory/goods/code"
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
        ret["summary"] = str(e)
    return HttpResponse(json.dumps(ret))


def linkman_photo(request):
    """联系人照片上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/inventory/linkman/photo"
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
        ret["summary"] = str(e)
    return HttpResponse(json.dumps(ret))


def goods_attach(request):
    """商品附件上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/inventory/goods/attach"
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


def linkman_card(request):
    """联系人名片上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/inventory/linkman/card"
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
        ret["summary"] = str(e)
    return HttpResponse(json.dumps(ret))


def linkman_attach(request):
    """商品附件上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/inventory/linkman/attach"
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


def supplier_photo(request):
    """供应商照片上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/inventory/supplier/photo"
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


def supplier_licence(request):
    """供应商执照上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/inventory/supplier/photo"
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


def supplier_attach(request):
    """商品附件上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/inventory/supplier/attach"
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


def contact_attach(request):
    """来往附件上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/inventory/supplier/contact"
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
