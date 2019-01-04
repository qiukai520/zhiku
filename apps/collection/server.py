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

    def query_record_by_origin(self,id):
        result_db=CollRecord.objects.filter(origin=id)
        return result_db


class CollRecordAttachDB(object):
    """收录附件表"""

    def query_task_submit_attachment_by_tsid(self,tsid):
        result_db = CollAttachment.objects.filter(tsid=tsid).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            CollAttachment.objects.create(**item)


coll_record_db = CollRecordDB()
record_attach_db = CollRecordAttachDB()