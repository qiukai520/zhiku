from django.shortcuts import render,HttpResponse
from django.core import serializers
from common.functions import *
from .forms.form import *
from .server import *

# Create your views here.


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


def country_town(request):
    """根据县区获取街道"""
    ret = {"status":False,"data":"","message":""}
    id = request.GET.get("id")
    if id:
        town_list = town_db.query_town_by_country(id)
        # 序列化queryset对象
        data = serializers.serialize("json", town_list)
        ret['status'] = True
        ret["data"] = data
    else:
        ret['message'] = "请选择相应的县区"
    return HttpResponse(json.dumps(ret))


def town_list(request):
    query_sets = town_db.query_town_list()
    return render(request,"inventory/town_list.html",{"query_sets":query_sets})


def town_edit(request):
    """"县区添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            obj = town_db.query_town_by_id(id)
        else:
            id = 0
            obj = []
        return render(request, 'inventory/town_edit.html', {"obj": obj, "id": id})
    else:
        form = TownForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", 0)
            data = request.POST
            data = data.dict()
            print(data)
            # data["country_id"] = int(data["country_id"])
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = town_db.query_town_by_id(id)
                    final_info = compare_fields(Town._update,record,data)
                    if final_info:
                        final_info["nid"] = id
                        final_info["country_id"] = data["country_id"]
                        final_info["town"] = data["town"]

                        town_db.update_town(final_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    print(e)
                    ret['message'] = str(e)
            else:
                try:
                    print('insert',data)
                    town_db.insert_town(data)
                    ret['status'] = True
                except Exception as e:
                    print(e)
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

