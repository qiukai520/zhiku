# -*- coding: utf-8 -*-
__author__ = 'lizhihong'

#独立使用django的model
import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))

sys.path.append(pwd+"../")
# 加载配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thinking_library.settings")

import django
django.setup()

from public.models import Province,City,Country,Town

from db_tools.data.pcas_data import region_data


for province in region_data:
    pro_intance = Province()
    pro_intance.code = province["code"]
    pro_intance.province = province["name"]
    pro_intance.save()
    province_id = pro_intance.nid

    for city in province["children"]:
        city_intance = City()
        city_intance.code = city["code"]
        city_intance.city = city["name"]
        city_intance.province_id = province_id
        city_intance.save()
        city_id = city_intance.nid

        for country in city["children"]:
            cy_intance = Country()
            cy_intance.code = country["code"]
            cy_intance.country = country["name"]
            cy_intance.city_id = city_id
            cy_intance.save()
            country_id = cy_intance.nid
            for town in country["children"]:
                town_intance = Town()
                town_intance.code = town["code"]
                town_intance.town = town["name"]
                town_intance.country_id = country_id
                town_intance.save()

print("done")

