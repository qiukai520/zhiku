from django.db import connection
from .models import *


class RevenueDB(object):
    """收录"""
    def insert_info(self, modify_info):
        revenue_sql = """insert into revenue(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        revenue_sql = revenue_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(revenue_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_revenue_list(self):
        result_db = Revenue.objects.filter().all()
        return result_db

    def query_revenue_by_list(self):
        result_db = Revenue.objects.filter().all().order_by("-nid")
        return result_db

    def query_revenue_by_id(self, id):
        result_db = Revenue.objects.filter(nid=id).first()
        return result_db

    def query_revenue_by_r_id(self, nid):
        result_db = Revenue.objects.filter(nid=nid).all().order_by("-nid")
        return result_db

    def query_revenue_by_origin(self,id):
        result_db = Revenue.objects.filter(origin=id)
        return result_db

    def query_revenue_by_type(self,id):
        result_db = Revenue.objects.filter(company=id).all()
        return result_db

    def update_info(self,modify_info):
        Revenue.objects.filter(nid=modify_info["nid"]).update(**modify_info)

    def multi_delete(self,id_list):
        Revenue.objects.filter(nid__in=id_list).delete()

class RevenueAttachDB(object):
    def query_revenue_attachment(self, id):
        result_db = RevenueAttach.objects.filter(sid=id).all()
        return result_db

    def query_revenue_attachment_by_sid(self, sid):
        result_db = RevenueAttach.objects.filter(sid_id=sid).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            RevenueAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            RevenueAttach.objects.filter(said=item['said']).update(**item)

    def mutil_delete_task_attachment(self, id_list):
        RevenueAttach.objects.filter(nid__in=id_list).delete()

    def multi_delete_attach_by_edit_id(self, id_list):
        RevenueAttach.objects.filter(sid_id__in=id_list).filter().delete()


class IncomeClassifyDB(object):
    def query_classify_list(self):
        result_db = Income_classify.objects.filter().all()
        return result_db

    def query_classify_by_id(self,id):
        result_db = Income_classify.objects.filter(id=id).first()
        return result_db

    def update_classify_title(self, modify_info):
        is_exist = Income_classify.objects.filter(name=modify_info['name']).first()
        if is_exist:
            raise Exception("该名称已存在")
        Income_classify.objects.filter(id=modify_info['id']).update(**modify_info)

    def insert_classify_title(self, modify_info):
        is_exist = Income_classify.objects.filter(name=modify_info['name']).first()
        if is_exist:
            raise Exception("该名称已存在")
        Income_classify.objects.create(**modify_info)

    def multi_delete(self,id_list):
        Income_classify.objects.filter(id__in=id_list).delete()



class AssociatesDB(object):
    def query_associates_list(self):
        result_db = Associates.objects.filter().all()
        return result_db

    def query_associates_by_id(self, id):
        result_db = Associates.objects.filter(id=id).first()
        return result_db

    def update_associates_title(self, modify_info):
        is_exist = Associates.objects.filter(name=modify_info['name']).first()
        if is_exist:
            raise Exception("该名称已存在")
        Associates.objects.filter(id=modify_info['id']).update(**modify_info)

    def insert_associates_title(self, modify_info):
        is_exist = Associates.objects.filter(name=modify_info['name']).first()
        if is_exist:
            raise Exception("该名称已存在")
        Associates.objects.create(**modify_info)

    def multi_delete(self,id_list):
        Associates.objects.filter(id__in=id_list).delete()


class Approver2DB(object):
    def query_approver2_list(self):
        result_db = Approver2.objects.filter().all()
        return result_db

    def query_approver2_by_id(self,id):
        result_db = Approver2.objects.filter(id=id).first()
        return result_db

    def query_approver2_by_department_id(self, department_id):
        result_db = Approver2.objects.filter(department_id=department_id).all()
        return result_db


# 支出管理
class DisbursementDB(object):
    """收录"""

    def insert_info(self, modify_info):
        disbur_sql = """insert into disbursement(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        disbur_sql = disbur_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(disbur_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_disbur_list(self):
        result_db = Disbursement.objects.filter().all()
        return result_db

    def query_disbur_by_list(self):
        result_db = Disbursement.objects.filter().all().order_by("-nid")
        return result_db

    def query_disbur_by_id(self, id):
        result_db = Disbursement.objects.filter(nid=id).first()
        return result_db

    def query_disbur_by_r_id(self, nid):
        result_db = Disbursement.objects.filter(nid=nid).all().order_by("-nid")
        return result_db

    def query_disbur_by_origin(self, id):
        result_db = Disbursement.objects.filter(origin=id)
        return result_db

    def query_disbur_by_type(self, id):
        result_db = Disbursement.objects.filter(company=id).all()
        return result_db

    def update_info(self, modify_info):
        Disbursement.objects.filter(nid=modify_info["nid"]).update(**modify_info)

    def multi_delete(self, id_list):
        Disbursement.objects.filter(nid__in=id_list).delete()

class DisburAttachDB(object):
    def query_disbur_attachment(self, id):
        result_db = DisburAttach.objects.filter(sid=id).all()
        return result_db

    def query_disbur_attachment_by_sid(self, sid):
        result_db = DisburAttach.objects.filter(sid_id=sid).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            DisburAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            DisburAttach.objects.filter(said=item['said']).update(**item)

    def mutil_delete_task_attachment(self, id_list):
        DisburAttach.objects.filter(nid__in=id_list).delete()

    def multi_delete_attach_by_edit_id(self, id_list):
        DisburAttach.objects.filter(sid_id__in=id_list).filter().delete()




revenue_db = RevenueDB()
revenueattach_db = RevenueAttachDB()
incomeclassify_db = IncomeClassifyDB()
associates_db = AssociatesDB()
approver2_db = Approver2DB()
disbur_db = DisbursementDB()
disburattach_db = DisburAttachDB()
