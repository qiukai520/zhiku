from django.db import connection
from .models import *

class AssetsDB(object):
    def insert_info(self, modify_info):
        assets_sql = """insert into assets(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        assets_sql = assets_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(assets_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_assets_list(self):
        result_db = Assets.objects.filter().all()
        return result_db

    def query_assets_by_list(self):
        result_db = Assets.objects.filter().all().order_by("-nid")
        return result_db

    def query_assets_by_id(self, id):
        result_db = Assets.objects.filter(nid=id).first()
        return result_db

    def query_assets_by_a_id(self, nid):
        result_db = Assets.objects.filter(nid=nid).all().order_by("-nid")
        return result_db

    def query_assets_by_origin(self,id):
        result_db = Assets.objects.filter(origin=id)
        return result_db

    def query_assets_by_type(self,id):
        result_db = Assets.objects.filter(company=id).all()
        return result_db

    def update_info(self,modify_info):
        Assets.objects.filter(nid=modify_info["nid"]).update(**modify_info)

    def multi_delete(self,id_list):
        Assets.objects.filter(nid__in=id_list).delete()

class AssetsAttachDB(object):
    def query_assets_attachment(self, id):
        result_db = AssetsAttach.objects.filter(sid=id).all()
        return result_db

    def query_assets_attachment_by_sid(self, sid):
        result_db = AssetsAttach.objects.filter(sid_id=sid).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            AssetsAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            AssetsAttach.objects.filter(said=item['said']).update(**item)

    def mutil_delete_task_attachment(self, id_list):
        AssetsAttach.objects.filter(nid__in=id_list).delete()

    def multi_delete_attach_by_edit_id(self, id_list):
        AssetsAttach.objects.filter(sid_id__in=id_list).filter().delete()


class AssetsClassifyDB(object):
    def query_classify_list(self):
        result_db = AssetsClassify.objects.filter().all()
        return result_db

    def query_classify_by_id(self,id):
        result_db = AssetsClassify.objects.filter(id=id).first()
        return result_db

class SaveCoordinateDB(object):
    def query_coordinate_list(self):
        result_db = SaveCoordinate.objects.filter().all()
        return result_db

    def query_coordinate_by_id(self, id):
        result_db = SaveCoordinate.objects.filter(id=id).first()
        return result_db

class ProcurementNameDB(object):
    def query_procurement_list(self):
        result_db = ProcurementName.objects.filter().all()
        return result_db

    def query_procurement_by_id(self, id):
        result_db = ProcurementName.objects.filter(id=id).first()
        return result_db

class UserNameDB(object):
    def query_username_list(self):
        result_db = UserName.objects.filter().all()
        return result_db

    def query_username_by_id(self, id):
        result_db = UserName.objects.filter(id=id).first()
        return result_db

class AssetsStatusDB(object):
    def query_assets_status_list(self):
        result_db = AssetsStatus.objects.filter().all()
        return result_db

    def query_assets_status_by_id(self, id):
        result_db = AssetsStatus.objects.filter(id=id).first()
        return result_db


assets_db = AssetsDB()
assetsattach_db = AssetsAttachDB()
assetsclassify_db = AssetsClassifyDB()
save_coordinate_db = SaveCoordinateDB()
procurement_db = ProcurementNameDB()
username_db = UserNameDB()
assets_status_db = AssetsStatusDB()