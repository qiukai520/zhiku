from django.db import connection
from .models import *


class SupplierDB(object):
    """员工表"""
    gender_choice = ({"id": 0, "caption": "男"}, {"id": 1, "caption": "女"})

    def insert_staff(self, modify_info):
        staff_sql = """insert into supplier(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        staff_sql = staff_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(staff_sql, modify_info)
        sid = cursor.lastrowid
        return sid

    def query_supplier_list(self):
        result_db = Supplier.objects.filter(delete_status=1).all()
        return result_db

    def query_supplier_by_id(self, nid):
        result_db = Supplier.objects.filter(nid=nid,delete_status=1).first()
        return result_db


    def update_supplier(self, modify):
        Supplier.objects.filter(nid=modify['nid'],delete_status=1).update(**modify)

    def multi_delete(self, id_list, delete_status):
        Supplier.objects.filter(nid__in=id_list).update(**delete_status)


class IndustryDB(object):
    """部门表"""
    def query_industry_list(self):
        result_db = Industry.objects.filter().all()
        return result_db

    def query_industry_by_id(self, nid):
        result_db = Industry.objects.filter(nid=nid).first()
        return result_db

    def update_industry(self, modify_info):
        is_exist = Industry.objects.filter(industry=modify_info['industry']).first()
        if is_exist:
            raise Exception("该行业名称已存在")
            Industry.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_industry(self, modify_info):
        is_exist = Industry.objects.filter(industry=modify_info['industry']).first()
        if is_exist:
            raise Exception("该行业名称已存在")
        Industry.objects.create(**modify_info)


class SupplierCategoryDB(object):
    """供应商分类"""
    def query_category_list(self):
        result_db = SupplierCategory.objects.filter().all()
        return result_db

    def query_category_by_id(self, nid):
        result_db = SupplierCategory.objects.filter(nid=nid).first()
        return result_db

    def update_category(self, modify_info):
        is_exist = SupplierCategory.objects.filter(caption=modify_info['caption']).first()
        if is_exist:
            raise Exception("该供应商分类名称已存在")
        SupplierCategory.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_category(self, modify_info):
        is_exist = SupplierCategory.objects.filter(caption=modify_info['caption']).first()
        if is_exist:
            raise Exception("该供应商分类名称已存在")
        SupplierCategory.objects.create(**modify_info)


class GoodsCategoryDB(object):
    """供应商分类"""
    def query_category_list(self):
        result_db = GoodsCategory.objects.filter().all()
        return result_db

    def query_category_by_id(self, nid):
        result_db = GoodsCategory.objects.filter(nid=nid).first()
        return result_db

    def update_category(self, modify_info):
        is_exist = GoodsCategory.objects.filter(caption=modify_info['caption']).first()
        if is_exist:
            raise Exception("该商品分类名称已存在")
        GoodsCategory.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_category(self, modify_info):
        is_exist = GoodsCategory.objects.filter(caption=modify_info['caption']).first()
        if is_exist:
            raise Exception("该商品分类名称已存在")
        GoodsCategory.objects.create(**modify_info)


class NationDB(object):
    """国家"""
    def query_nation_list(self):
        result_db = Nation.objects.filter().all()
        return result_db

    def query_nation_by_id(self, nid):
        result_db = Nation.objects.filter(nid=nid).first()
        return result_db

    def update_nation(self, modify_info):
        is_exist = Nation.objects.filter(nation=modify_info['nation']).first()
        if is_exist:
            raise Exception("该国家已存在")
        Nation.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_nation(self, modify_info):
        is_exist = Nation.objects.filter(nation=modify_info['nation']).first()
        if is_exist:
            raise Exception("该国家已存在")
        Nation.objects.create(**modify_info)


class ProvinceDB(object):
    """省份"""
    def __init__(self):
        pass

    def query_province_list(self):
        result_db = Province.objects.filter().all()
        return result_db

    def query_province_by_id(self, nid):
        result_db = Province.objects.filter(nid=nid).first()
        return result_db

    def update_province(self, modify_info):
        is_exist = self.is_exist(modify_info["province"], modify_info["nation_id"])
        if is_exist:
            raise Exception("该省份已存在")
        Province.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_province(self, modify_info):
        is_exist = self.is_exist(modify_info["province"],modify_info["nation_id"])
        if is_exist:
            raise Exception("该省份已存在")
        Province.objects.create(**modify_info)

    def is_exist(self,province,nation):
        result_db = Province.objects.filter(province=province, nation_id=nation).first()
        return result_db


supplier_db = SupplierDB()
industry_db = IndustryDB()
supplier_category_db = SupplierCategoryDB()
goods_category_db = GoodsCategoryDB()
nation_db = NationDB()
province_db = ProvinceDB()


