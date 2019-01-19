from django.db import connection
from .models import *



class ContractFollowDB(object):
    """客户跟进记录"""

    def insert_follow(self, modify_info):
        follow_sql = """insert into contract_follow(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        follow_sql = follow_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(follow_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_list(self):
        result_db = ContractFollow.objects.filter().all()
        return result_db

    def query_follow_by_id(self, nid):
        result_db = ContractFollow.objects.filter(nid=nid).first()
        return result_db

    def query_follow_by_contract_id(self, cid):
        result_db = ContractFollow.objects.filter(contract_id=cid).all().order_by("-nid")
        return result_db

    def update_follow(self, modify):
        ContractFollow.objects.filter(nid=modify['nid']).update(**modify)

    def multi_delete(self, id_list):
        ContractFollow.objects.filter(nid__in=id_list).delete()



class FollowAttachDB(object):
    """跟踪附件表"""
    def query_follow_attachment_list(self):
        result_db = ContractFollowAttach.objects.filter().all()
        return result_db

    def query_follow_attachment(self,id):
        result_db = ContractFollowAttach.objects.filter(follow_id=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            ContractFollowAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            ContractFollowAttach.objects.filter(nid=item['nid']).update(**item)

    def mutil_delete_follow_attachment(self, id_list):
        ContractFollowAttach.objects.filter(nid__in=id_list).delete()

    def multi_delete_attach_by_follow_id(self,id_list):
        ContractFollowAttach.objects.filter(follow_id__in=id_list).filter().delete()

    def delete_attachment(self,nid):
        ContractFollowAttach.objects.filter(nid=nid).delete()


crt_follow_db = ContractFollowDB()
crt_follow_attach_db = ContractFollowAttach()