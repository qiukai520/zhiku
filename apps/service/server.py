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


class FollowWayDB(object):
    """跟进方式"""
    def query_way_list(self):
        result_db = FollowWay.objects.filter().all()
        return result_db

    def query_way_by_id(self,id):
        result_db = FollowWay.objects.filter(nid=id).first()
        return result_db

    def update_way(self, modify_info):
        is_exist = FollowWay.objects.filter(content=modify_info['content']).first()
        if is_exist:
            raise Exception("该名称已存在")
        FollowWay.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_way(self, modify_info):
        is_exist = FollowWay.objects.filter(content=modify_info['content']).first()
        if is_exist:
            raise Exception("该名称已存在")
        FollowWay.objects.create(**modify_info)


class FollowContactDB(object):
    """联络方式"""
    def query_contact_list(self):
        result_db = FollowContact.objects.filter().all()
        return result_db

    def query_contact_by_id(self,id):
        result_db = FollowContact.objects.filter(nid=id).first()
        return result_db

    def query_contact_by_follow_id(self,id):
        result_db = FollowContact.objects.filter(nid=id).first()
        return result_db

    def update_contact(self, modify_info):
        is_exist = FollowContact.objects.filter(content=modify_info['content']).first()
        if is_exist:
            raise Exception("该名称已存在")
        FollowContact.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_contact(self, modify_info):
        is_exist = FollowContact.objects.filter(content=modify_info['content']).first()
        if is_exist:
            raise Exception("该名称已存在")
        FollowContact.objects.create(**modify_info)


crt_follow_db = ContractFollowDB()
crt_follow_attach_db = FollowAttachDB()
way_db = FollowWayDB()
contact_db = FollowContactDB()