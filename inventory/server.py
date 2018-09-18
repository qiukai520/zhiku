from django.db import connection
from .models import *





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
    """商品分类"""
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


class GoodsUnitDB(object):
    """商品单位"""
    def query_unit_list(self):
        result_db = GoodsUnit.objects.filter().all()
        return result_db

    def query_unit_by_id(self, nid):
        result_db = GoodsUnit.objects.filter(nid=nid).first()
        return result_db

    def update_unit(self, modify_info):
        is_exist = GoodsUnit.objects.filter(caption=modify_info['caption']).first()
        if is_exist:
            raise Exception("该商品单位已存在")
        GoodsUnit.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_unit(self, modify_info):
        is_exist = GoodsUnit.objects.filter(caption=modify_info['caption']).first()
        if is_exist:
            raise Exception("该商品单位已存在")
        GoodsUnit.objects.create(**modify_info)


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

    def query_province_by_nation(self,nation_id):
        result_db=Province.objects.filter(nation_id=nation_id).all()
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


class CityDB(object):
    """城市"""
    def __init__(self):
        pass

    def query_city_list(self):
        result_db = City.objects.filter().all()
        return result_db

    def query_city_by_id(self, nid):
        result_db = City.objects.filter(nid=nid).first()
        return result_db

    def query_city_by_province(self, province_id):
        result_db = City.objects.filter(province_id=province_id).all()
        return result_db

    def update_city(self, modify_info):
        is_exist = self.is_exist(modify_info["province_id"], modify_info["city"])
        if is_exist:
            raise Exception("该城市已存在")
        City.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_city(self, modify_info):
        is_exist = self.is_exist(modify_info["province_id"],modify_info["city"])
        if is_exist:
            raise Exception("该城市已存在")
        City.objects.create(**modify_info)

    def is_exist(self,province,city):
        result_db = City.objects.filter(province_id=province, city=city).first()
        return result_db


class CountryDB(object):
    """县区"""
    def __init__(self):
        pass

    def query_country_list(self):
        result_db = Country.objects.filter().all()
        return result_db

    def query_country_by_id(self, nid):
        result_db = Country.objects.filter(nid=nid).first()
        return result_db

    def query_country_by_city(self, city_id):
        result_db = Country.objects.filter(city_id=city_id).all()
        return result_db

    def update_country(self, modify_info):
        is_exist = self.is_exist(modify_info["country"], modify_info["city_id"])
        if is_exist:
            raise Exception("该县区已存在")
        Country.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_country(self, modify_info):
        is_exist = self.is_exist(modify_info["country"],modify_info["city_id"])
        if is_exist:
            raise Exception("该县区已存在")
        Country.objects.create(**modify_info)

    def is_exist(self,country,city_id):
        result_db = Country.objects.filter(country=country, city_id=city_id).first()
        return result_db


class GoodsDB(object):
    """商品表"""
    def insert_goods(self,modify_info):
        staff_sql = """insert into goods(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        staff_sql = staff_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(staff_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_goods_list(self):
        result_db = Goods.objects.filter(delete_status=1).all()
        return result_db

    def query_goods_by_id(self, nid):
        result_db = Goods.objects.filter(nid=nid,delete_status=1).first()
        return result_db

    def query_goods_by_category(self, category_id):
        result_db = Goods.objects.filter(category_id=category_id,delete_status=1).all()
        return result_db

    def update_goods(self, modify):
        Goods.objects.filter(nid=modify['nid'],delete_status=1).update(**modify)

    def multi_delete(self, id_list, delete_status):
        Goods.objects.filter(nid__in=id_list).update(**delete_status)


class GoodsPhotoDB(object):
    """商品图片"""

    def insert_photo(self, modify):
        GoodsPhoto.objects.create(**modify)

    def query_goods_photo(self,id):
        result_db = GoodsPhoto.objects.filter(goods_id=id).first()
        return result_db

    def update_photo(self, modify):
        GoodsPhoto.objects.filter(goods_id=modify["goods_id"]).update(**modify)

    def delete_photo_by_goods_id(self, id):
        GoodsPhoto.objects.filter(goods_id=id).delete()


class GoodsBarCodeDB(object):
    """商品条码"""

    def insert_bar(self, modify):
        GoodsBarCode.objects.create(**modify)

    def query_goods_bar(self,id):
        result_db = GoodsBarCode.objects.filter(goods_id=id).first()
        return result_db

    def update_bar(self, modify):
        GoodsBarCode.objects.filter(goods_id=modify["goods_id"]).update(**modify)

    def delete_photo_by_goods_id(self, id):
        GoodsBarCode.objects.filter(goods_id=id).delete()


class GoodsAttachDB(object):
    """商品附件表"""
    def query_goods_attachment_list(self):
        result_db = GoodsAttach.objects.filter().all()
        return result_db

    def query_goods_attachment(self,id):
        result_db = GoodsAttach.objects.filter(goods_id=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            GoodsAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            GoodsAttach.objects.filter(nid=item['nid']).update(**item)

    def mutil_delete_goods_attachment(self, id_list):
        GoodsAttach.objects.filter(nid__in=id_list).delete()

    def multi_delete_attach_by_goods_id(self,id_list):
        GoodsAttach.objects.filter(goods_id__in=id_list).filter().delete()

    def delete_goods_attachment(self,nid):
        GoodsAttach.objects.filter(nid=nid).delete()


class SupplierDB(object):
    """供应商表"""
    gender_choice = ({"id": 0, "caption": "男"}, {"id": 1, "caption": "女"})

    def insert_supplier(self, modify_info):
        supplier_sql = """insert into supplier(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        supplier_sql = supplier_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(supplier_sql, modify_info)
        nid = cursor.lastrowid
        return nid

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


class SupplierPhotoDB(object):
    """供应商图片"""

    def insert_photo(self, modify):
        SupplierPhoto.objects.create(**modify)

    def query_supplier_photo(self,id):
        result_db = SupplierPhoto.objects.filter(supplier_id=id).first()
        return result_db

    def update_photo(self, modify):
        SupplierPhoto.objects.filter(supplier_id=modify["supplier_id"]).update(**modify)

    def delete_photo_by_supplier_id(self, id):
        SupplierPhoto.objects.filter(supplier_id=id).delete()


class SupplierLicenceDB(object):
    """商品营业执照"""

    def insert_photo(self, modify):
        SupplierLicence.objects.create(**modify)

    def query_supplier_licence(self,id):
        result_db = SupplierLicence.objects.filter(supplier_id=id).first()
        return result_db

    def update_licence(self, modify):
        SupplierLicence.objects.filter(supplier_id=modify["supplier_id"]).update(**modify)

    def delete_licence_by_supplier_id(self,id):
        SupplierLicence.objects.filter(supplier_id=id).delete()


class SupplierAttachDB(object):
    """供应商附件表"""
    def query_supplier_attachment_list(self):
        result_db = SupplierAttach.objects.filter().all()
        return result_db

    def query_supplier_attachment(self,id):
        result_db = SupplierAttach.objects.filter(supplier_id=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            SupplierAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            SupplierAttach.objects.filter(nid=item['nid']).update(**item)

    def mutil_delete_supplier_attachment(self, id_list):
        SupplierAttach.objects.filter(nid__in=id_list).delete()

    def multi_delete_attach_by_supplier_id(self,id_list):
        SupplierAttach.objects.filter(supplier_id__in=id_list).filter().delete()

    def delete_supplier_attachment(self,nid):
        SupplierAttach.objects.filter(nid=nid).delete()



class LinkmanDB(object):
    """联系人表"""
    gender_choice = ({"id": 0, "caption": "男"}, {"id": 1, "caption": "女"})
    marriage_choice = ({"id": 0, "caption": "未婚"}, {"id": 1, "caption": "已婚"})

    def insert_linkman(self, modify_info):
        linkman_sql = """insert into linkman(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        linkman_sql = linkman_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(linkman_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_linkman_list(self):
        result_db = Linkman.objects.filter(delete_status=1).all()
        return result_db

    def query_linkman_by_id(self, nid):
        result_db = Linkman.objects.filter(nid=nid,delete_status=1).first()
        return result_db

    def query_linkman_by_supplier_id(self,id):
        result_db = Linkman.objects.filter(supplier_id=id, delete_status=1).all()
        return result_db

    def update_linkman(self, modify):
        Linkman.objects.filter(nid=modify['nid'],delete_status=1).update(**modify)

    def multi_delete(self, id_list, delete_status):
        Linkman.objects.filter(nid__in=id_list).update(**delete_status)


class SupplierContactDB(object):
    """供应商来往"""
    category= ({"id": 0, "caption": "交易收入"}, {"id": 1, "caption": "商务支出"})

    def insert_contact(self, modify_info):
        contact_sql = """insert into supplier_contact(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        contact_sql = contact_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(contact_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_contact_list(self):
        result_db = SupplierContact.objects.filter(delete_status=1).all()
        return result_db

    def query_contact_by_id(self, nid):
        result_db = SupplierContact.objects.filter(nid=nid,delete_status=1).first()
        return result_db

    def query_contact_by_supplier(self,supplier_id):
        result_db = SupplierContact.objects.filter(supplier_id=supplier_id, delete_status=1)
        return result_db

    def update_contact(self, modify):
        SupplierContact.objects.filter(nid=modify['nid'],delete_status=1).update(**modify)

    def multi_delete(self, id_list, delete_status):
        SupplierContact.objects.filter(nid__in=id_list).update(**delete_status)


class ContactAttachDB(object):
    """来往附件表"""
    def query_contact_attachment_list(self):
        result_db = ContactAttach.objects.filter().all()
        return result_db

    def query_contact_attachment(self, id):
        print("id",id)
        result_db = ContactAttach.objects.filter(contact_id=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            ContactAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            ContactAttach.objects.filter(nid=item['nid']).update(**item)

    def mutil_delete_linkman_attachment(self, id_list):
        ContactAttach.objects.filter(nid__in=id_list).delete()

    def multi_delete_attach_by_linkman_id(self,id_list):
        ContactAttach.objects.filter(linkman_id__in=id_list).filter().delete()

    def delete_contact_attachment(self,nid):
        ContactAttach.objects.filter(nid=nid).delete()


class LinkmanPhotoDB(object):
    """供应商图片"""

    def insert_photo(self, modify):
        LinkmanPhoto.objects.create(**modify)

    def query_linkman_photo(self,id):
        result_db = LinkmanPhoto.objects.filter(linkman_id=id).first()
        return result_db

    def update_photo(self, modify):
        LinkmanPhoto.objects.filter(linkman_id=modify["linkman_id"]).update(**modify)

    def delete_photo_by_linkman_id(self, id):
        LinkmanPhoto.objects.filter(linkman_id=id).delete()


class LinkmanCardDB(object):
    """联系人卡片"""

    def insert_photo(self, modify):
        LinkmanCard.objects.create(**modify)

    def query_linkman_card(self,id):
        result_db = LinkmanCard.objects.filter(linkman_id=id).first()
        return result_db

    def update_card(self, modify):
        LinkmanCard.objects.filter(linkman_id=modify["linkman_id"]).update(**modify)

    def delete_card_by_card_id(self,id):
        LinkmanCard.objects.filter(linkman_id=id).delete()


class LinkmanAttachDB(object):
    """联系人附件表"""
    def query_linkman_attachment_list(self):
        result_db = LinkmanAttach.objects.filter().all()
        return result_db

    def query_linkman_attachment(self,id):
        result_db = LinkmanAttach.objects.filter(linkman_id=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            LinkmanAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            LinkmanAttach.objects.filter(nid=item['nid']).update(**item)

    def mutil_delete_linkman_attachment(self, id_list):
        LinkmanAttach.objects.filter(nid__in=id_list).delete()

    def multi_delete_attach_by_linkman_id(self,id_list):
        LinkmanAttach.objects.filter(linkman_id__in=id_list).filter().delete()

    def delete_linkman_attachment(self,nid):
        LinkmanAttach.objects.filter(nid=nid).delete()


supplier_db = SupplierDB()
supplier_photo_db = SupplierPhotoDB()
supplier_licence_db = SupplierLicenceDB()
supplier_attach_db = SupplierAttachDB()
supplier_contact_db = SupplierContactDB()
contact_attach_db = ContactAttachDB()
industry_db = IndustryDB()
supplier_category_db = SupplierCategoryDB()
goods_category_db = GoodsCategoryDB()
goods_unit_db = GoodsUnitDB()
nation_db = NationDB()
province_db = ProvinceDB()
city_db = CityDB()
country_db = CountryDB()
goods_db = GoodsDB()
goods_photo_db = GoodsPhotoDB()
goods_code_db = GoodsBarCodeDB()
goods_attach_db = GoodsAttachDB()
linkman_db = LinkmanDB()
linkman_photo_db = LinkmanPhotoDB()
linkman_card_db = LinkmanCardDB()
linkman_attach_db = LinkmanAttachDB()


