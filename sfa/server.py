from django.db import connection
from .models import *


class CustomerDB(object):
    """客户表"""
    purpose_choice = ({"id": 0, "caption": "A类客户"}, {"id": 1, "caption": "B类客户"},
                     {"id": 2, "caption": "C类客户"},{"id": 3, "caption": "D类客户"},
                     {"id": 4, "caption": "K类客户"},{"id":5, "caption": "K1类客户"},
                     {"id": 6, "caption": "K2类客户"})

    def insert_customer(self, modify_info):
        customer_sql = """insert into customer_info(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        customer_sql = customer_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(customer_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_list(self):
        result_db = CustomerInfo.objects.filter().all()
        return result_db

    def query_customer_by_id(self, nid):
        result_db = CustomerInfo.objects.filter(nid=nid).first()
        return result_db

    def update_customer(self, modify):
        CustomerInfo.objects.filter(nid=modify['nid']).update(**modify)

    # def multi_delete(self, id_list, delete_status):
    #     CustomerInfo.objects.filter(nid__in=id_list).update(**delete_status)


class CustomerCategoryDB(object):
    """客户分类"""
    def query_category_list(self):
        result_db = CustomerCategory.objects.filter().all()
        return result_db

    def query_category_by_id(self, nid):
        result_db = CustomerCategory.objects.filter(nid=nid).first()
        return result_db

    def update_category(self, modify_info):
        is_exist = CustomerCategory.objects.filter(caption=modify_info['caption']).first()
        if is_exist:
            raise Exception("该客户分类名称已存在")
        CustomerCategory.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_category(self, modify_info):
        is_exist = CustomerCategory.objects.filter(caption=modify_info['caption']).first()
        if is_exist:
            raise Exception("该客户分类名称已存在")
        CustomerCategory.objects.create(**modify_info)


class CustomerPhotoDB(object):
    """客户图片"""

    def insert_photo(self, modify):
        CustomerPhoto.objects.create(**modify)

    def query_customer_photo(self,id):
        result_db = CustomerPhoto.objects.filter(customer_id=id).first()
        return result_db

    def update_photo(self, modify):
        CustomerPhoto.objects.filter(customer_id=modify["customer_id"]).update(**modify)

    def delete_photo_by_customer_id(self, id):
        CustomerPhoto.objects.filter(customer_id=id).delete()


class CustomerLicenceDB(object):
    """客户营业执照"""

    def insert_photo(self, modify):
        print("modirfy",modify)
        CustomerLicence.objects.create(**modify)

    def query_customer_licence(self,id):
        result_db = CustomerLicence.objects.filter(customer_id=id).first()
        return result_db

    def update_licence(self, modify):
        CustomerLicence.objects.filter(customer_id=modify["customer_id"]).update(**modify)

    def delete_licence_by_customer_id(self,id):
        CustomerLicence.objects.filter(customer_id=id).delete()


class CustomerAttachDB(object):
    """客户附件表"""
    def query_customer_attachment_list(self):
        result_db = CustomerAttach.objects.filter().all()
        return result_db

    def query_customer_attachment(self,id):
        result_db = CustomerAttach.objects.filter(customer_id=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            CustomerAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            CustomerAttach.objects.filter(nid=item['nid']).update(**item)

    def mutil_delete_customer_attachment(self, id_list):
        CustomerAttach.objects.filter(nid__in=id_list).delete()

    def multi_delete_attach_by_customer_id(self,id_list):
        CustomerAttach.objects.filter(customer_id__in=id_list).filter().delete()

    def delete_customer_attachment(self,nid):
        CustomerAttach.objects.filter(nid=nid).delete()


customer_db = CustomerDB()
customer_category_db = CustomerCategoryDB()
customer_attach_db = CustomerAttachDB()
customer_licence_db = CustomerLicenceDB()
customer_photo_db = CustomerPhotoDB()