import uuid
import os
from django.db import transaction
from django.shortcuts import render,HttpResponse
from django.core import serializers
from .server import *
from .forms.form import *
from common.functions import *
# Create your views here.


def supplier_list(request):
    pass
    return render(request,'inventory/supplier_list.html')


def supplier_edit(request):
    return render(request,'inventory/supplier_edit.html')


def goods_list(request):
    query_sets = goods_db.query_goods_list()
    return render(request, 'inventory/goods_list.html',{"query_sets":query_sets})



def goods_edit(request):
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
        print("query_sets",query_sets)
        print("goods_code",goods_code.photo)
        print("goods_attach",goods_attach)
        print("ndi",nid)
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
            goods_photo = data.get("goods_photo", None)
            goods_code = data.get("goods_code", None)
            goods_attach = data.get("attach", None)
            nid = data.get("nid", None)
            goods_photo = json.loads(goods_photo)
            goods_code = json.loads(goods_code)
            goods_attach = list(json.loads(goods_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新人事信息
                        record = goods_db.query_goods_by_id(nid)
                        goods_info = compare_fields(Goods._update, record, data)
                        if goods_info:
                            goods_info["nid"] = nid
                            goods_db.update_goods(goods_info)
                        # 插入人事生活照
                        photo_record = goods_photo_db.query_goods_photo(nid)
                        if goods_photo:
                            # 数据对比
                            if photo_record:
                                final_photo = compare_fields(GoodsPhoto._update, photo_record, goods_photo)
                                final_photo["goods_id"] = nid
                                if final_photo:
                                    goods_photo_db.update_photo(final_photo)
                            else:
                                goods_photo_db.insert_photo(goods_photo)
                        else:
                            # 删除旧数据
                            if photo_record:
                                goods_photo_db.delete_photo_by_goods_id(nid)
                        if goods_code:
                            # 数据对比
                            if photo_record:
                                final_photo = compare_fields(GoodsBarCode._update, photo_record, goods_code)
                                final_photo["goods_id"] = nid
                                if final_photo:
                                    goods_code_db.update_bar(final_photo)
                            else:
                                goods_code_db.insert_bar(goods_code)
                        else:
                            # 删除旧数据
                            if photo_record:
                                goods_code_db.delete_photo_by_goods_id(nid)
                        if goods_attach:
                            # 更新附件
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
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "更新失败"
            else:
                print("添加")
                # 创建
                try:
                    with transaction.atomic():
                        # 插入人事信息
                        goods_info = filter_fields(Goods._insert, data)
                        nid = goods_db.insert_goods(goods_info)
                        print("nid",nid)
                        # 插入商品照片
                        if goods_photo:
                            print("photo")
                            goods_photo["goods_id"] = nid
                            goods_photo_db.insert_photo(goods_photo)
                        # 插入商品条码照
                        if goods_code:
                            goods_code["goods_id"] = nid
                            goods_code_db.insert_bar(goods_code)
                        if goods_attach:
                            print("att")
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


def supplier_category_list(request):
    query_sets = supplier_category_db.query_category_list()
    return render(request,"inventory/supplier_category_list.html",{"query_sets":query_sets})


def supplier_category_edit(request):
    """"供应商分类添加或编辑"""
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


def nation_list(request):
    query_sets = nation_db.query_nation_list()
    return render(request,"inventory/nation_list.html",{"query_sets":query_sets})


def nation_edit(request):
    """"国家添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            obj = nation_db.query_nation_by_id(id)
        else:
            id = 0
            obj = []
        return render(request, 'inventory/nation_edit.html', {"obj": obj, "id": id})
    else:
        form = NationForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", 0)
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = nation_db.query_nation_by_id(id)
                    final_info = compare_fields(Nation._update,record,data)
                    if final_info:
                        final_info["nid"] = id
                        nation_db.update_nation(final_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    nation_db.insert_nation(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def province_list(request):
    query_sets = province_db.query_province_list()
    return render(request,"inventory/province_list.html",{"query_sets":query_sets})


def province_edit(request):
    """"省份添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            obj = province_db.query_province_by_id(id)
        else:
            id = 0
            obj = []
        return render(request, 'inventory/province_edit.html', {"obj": obj, "id": id})
    else:
        form = ProvinceForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", 0)
            data = request.POST
            data = data.dict()
            data["nation_id"] = int(data["nation_id"])
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = province_db.query_province_by_id(id)
                    final_info = compare_fields(Province._update,record,data)
                    if final_info:
                        final_info["nid"] = id
                        final_info["nation_id"] = data["nation_id"]
                        final_info["province"] = data["province"]
                        province_db.update_province(final_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
            else:
                try:
                    province_db.insert_province(data)
                    ret['status'] = True
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def city_list(request):
    query_sets = city_db.query_city_list()
    return render(request,"inventory/city_list.html",{"query_sets":query_sets})

def city_edit(request):
    """"省份添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            obj = city_db.query_city_by_id(id)
        else:
            id = 0
            obj = []
        return render(request, 'inventory/city_edit.html', {"obj": obj, "id": id})
    else:
        form = CityForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", 0)
            data = request.POST
            data = data.dict()
            data["province_id"] = int(data["province_id"])
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = city_db.query_city_by_id(id)
                    final_info = compare_fields(City._update,record,data)
                    if final_info:
                        final_info["nid"] = id
                        final_info["province_id"] = data["province_id"]
                        final_info["city"] = data["city"]
                        city_db.update_city(final_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
            else:
                try:
                    city_db.insert_city(data)
                    ret['status'] = True
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def country_list(request):
    query_sets = country_db.query_country_list()
    return render(request,"inventory/country_list.html",{"query_sets":query_sets})

def country_edit(request):
    """"县区添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            obj = country_db.query_country_by_id(id)
        else:
            id = 0
            obj = []
        return render(request, 'inventory/country_edit.html', {"obj": obj, "id": id})
    else:
        form = CountryForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", 0)
            data = request.POST
            data = data.dict()
            data["city_id"] = int(data["city_id"])
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = country_db.query_country_by_id(id)
                    final_info = compare_fields(Country._update,record,data)
                    if final_info:
                        final_info["nid"] = id
                        final_info["city_id"] = data["city_id"]
                        final_info["country"] = data["country"]
                        country_db.update_country(final_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
            else:
                try:
                    country_db.insert_country(data)
                    ret['status'] = True
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def nation_province(request):
    """根据国家获取省份"""
    ret = {"status":False,"data":"","message":""}
    id =request.GET.get("id")
    if id:
        province_list =province_db.query_province_by_nation(id)
        # 序列化queryset对象
        data = serializers.serialize("json", province_list)
        ret['status'] = True
        ret["data"]= data
    else:
        ret['message'] = "请选择相应的国家"

    return HttpResponse(json.dumps(ret))


def province_city(request):
    """根据省份获取城市"""
    ret = {"status":False,"data":"","message":""}
    id = request.GET.get("id")
    if id:
        city_list = city_db.query_city_by_province(id)
        # 序列化queryset对象
        data = serializers.serialize("json", city_list)
        ret['status'] = True
        ret["data"] = data
    else:
        ret['message'] = "请选择相应的省份"
    return HttpResponse(json.dumps(ret))


def city_country(request):
    """根据城市获取县区"""
    ret = {"status":False,"data":"","message":""}
    id = request.GET.get("id")
    if id:
        country_list = country_db.query_country_by_city(id)
        # 序列化queryset对象
        data = serializers.serialize("json", country_list)
        ret['status'] = True
        ret["data"] = data
    else:
        ret['message'] = "请选择相应的城市"
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

