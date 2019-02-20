from django.db import connection
from .models import *


class FileDB(object):
    """员工表"""
    gender_choice = ({"id": 0, "caption": "男"}, {"id": 1, "caption": "女"})
    lunar_choice = ({"id": 0, "caption": "公历"}, {"id": 1, "caption": "农历"})

    def insert_file(self,modify_info):
        file_sql = """insert into file(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        staff_sql = file_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(staff_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_file_list(self):
        result_db = File.objects.filter().all()

        return result_db


class TagDB(object):
    """标签"""
    def query_tag_list(self):
        result_db = FileTag.objects.filter().all()
        return result_db

    def query_tag_by_id(self,id):
        result_db = FileTag.objects.filter(id=id).first()
        return result_db

    def update_tag(self, modify_info):
        is_exist = FileTag.objects.filter(name=modify_info['name']).first()
        if is_exist:
            raise Exception("该标签名称已存在")
        FileTag.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_tag(self, modify_info):
        is_exist = FileTag.objects.filter(name=modify_info['name']).first()
        if is_exist:
            raise Exception("该标签名称已存在")
        FileTag.objects.create(**modify_info)


class File2TagDB(object):
    """文件标签关系表"""
    def mutil_insert(self, modify_info):
        for item in modify_info:
            Membership.objects.get_or_create(**item)


tag_db = TagDB()
file_db = FileDB()
file2tag_db = File2TagDB()