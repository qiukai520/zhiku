from django.db import connection
from .models import *


class CollRecordDB(object):
    """收录"""
    def insert_record(self, modify_info):
        record_sql = """insert into coll_record(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        record_sql = record_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(record_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_record_list(self):
        result_db = CollRecord.objects.filter().all()
        return result_db

    def query_record_by_id(self, id):
        result_db = CollRecord.objects.filter(nid=id).first()
        return result_db

    def query_record_by_origin(self,id):
        result_db = CollRecord.objects.filter(origin=id)
        return result_db

    def query_record_by_type(self,id):
        result_db = CollRecord.objects.filter(type=id).all()
        return result_db

    def update_info(self,modify_info):
        CollRecord.objects.filter(nid=modify_info["nid"]).update(**modify_info)

    def multi_delete(self,id_list):
        CollRecord.objects.filter(nid__in=id_list).delete()


class CollRecordAttachDB(object):
    """收录附件表"""

    def query_record_attach_by_tsid(self,tsid):
        result_db = CollAttachment.objects.filter(tsid=tsid).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            CollAttachment.objects.create(**item)

    def mutil_delete(self,id_list):
        CollAttachment.objects.filter(nid__in=id_list).delete()

    def mutil_delete_by_tsid(self, tsid):
        CollAttachment.objects.filter(tsid_id=tsid).delete()

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            CollAttachment.objects.filter(nid=item['nid']).update(**item)


class CollFavorDB(object):
    """点赞"""
    def is_exist(self, modify):
        result_db = CollFavor.objects.filter(tsid=modify["tsid_id"], uid=modify["uid_id"])
        return result_db

    def insert_favor(self,modiy_info):
        CollFavor.objects.get_or_create(**modiy_info)

    def count_favor(self,tsid):
        sql = """select sum(status) as count from  coll_favor  where tsid_id={0} GROUP BY tsid_id;""".format(tsid)
        cursor = connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        return row


coll_record_db = CollRecordDB()
record_attach_db = CollRecordAttachDB()
coll_favor_db = CollFavorDB()