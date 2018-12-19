from django.db import connection
from django.db.models import Sum
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


class SupplierMemoDB(object):
    """供应商备忘"""
    def insert_memo(self, modify_info):
        memo_sql = """insert into supplier_memo(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        memo_sql = memo_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(memo_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_memo_list(self):
        result_db = SupplierMemo.objects.filter().all()
        return result_db

    def query_memo_by_id(self, nid):
        result_db = SupplierMemo.objects.filter(nid=nid).first()
        return result_db

    def query_memo_by_supplier_id(self, sid):
        result_db = SupplierMemo.objects.filter(supplier_id=sid).all()
        return result_db

    def update_memo(self, modify_info):
        SupplierMemo.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def multi_delete(self,id_list):
        SupplierMemo.objects.filter(nid__in=id_list).delete()


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


class GoodsPriceDB(object):
    """商品比价"""

    def insert_price(self, modify_info):
        price_sql = """insert into goods_price(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        price_sql = price_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(price_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_price_list(self):
        result_db = GoodsPrice.objects.filter(delete_status=1).all()
        return result_db

    def query_price_by_id(self, nid):
        result_db = GoodsPrice.objects.filter(nid=nid, delete_status=1).first()
        return result_db

    def query_price_by_goods(self,goods_id):
        result_db = GoodsPrice.objects.filter(goods_id=goods_id, delete_status=1)
        return result_db

    def update_price(self, modify):
        GoodsPrice.objects.filter(nid=modify['nid'], delete_status=1).update(**modify)

    def multi_delete(self, id_list, delete_status):
        GoodsPrice.objects.filter(nid__in=id_list).update(**delete_status)


class PriceCompareDB(object):
    """商品比价"""

    def insert_price(self, modify_info):
        price_sql = """insert into price_compare(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        price_sql = price_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(price_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_price_list(self):
        result_db = PriceCompare.objects.filter(delete_status=1).all()
        return result_db

    def query_price_by_id(self, nid):
        result_db = PriceCompare.objects.filter(nid=nid,delete_status=1).first()
        return result_db

    def query_price_by_goods(self,goods_id):
        result_db = PriceCompare.objects.filter(goods_id=goods_id, delete_status=1)
        return result_db

    def update_price(self, modify):
        PriceCompare.objects.filter(nid=modify['nid'], delete_status=1).update(**modify)

    def multi_delete(self, id_list, delete_status):
        PriceCompare.objects.filter(nid__in=id_list).update(**delete_status)


class PriceAttachDB(object):
    """备忘附件表"""
    def query_price_attachment_list(self):
        result_db = PriceAttach.objects.filter().all()
        return result_db

    def query_price_attachment(self, id):
        result_db = PriceAttach.objects.filter(price_id=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            PriceAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            PriceAttach.objects.filter(nid=item['nid']).update(**item)

    def mutil_delete_price_attachment(self, id_list):
        PriceAttach.objects.filter(nid__in=id_list).delete()

    def multi_delete_attach_by_price_id(self,id_list):
        PriceAttach.objects.filter(price_id__in=id_list).filter().delete()

    def delete_price_attachment(self,nid):
        PriceAttach.objects.filter(nid=nid).delete()


class RetailSupplierDB(object):
    """零售供应商"""
    def query_retail_list(self):
        result_db = RetailSupplier.objects.filter().all()
        return result_db

    def query_retail_by_id(self, nid):
        result_db = RetailSupplier.objects.filter(nid=nid).first()
        return result_db

    def update_retail(self, modify_info):
        is_exist = RetailSupplier.objects.filter(caption=modify_info['caption']).first()
        if is_exist:
            raise Exception("该零售商已存在")
        RetailSupplier.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_retail(self, modify_info):
        is_exist = RetailSupplier.objects.filter(caption=modify_info['caption']).first()
        if is_exist:
            raise Exception("该零售已存在")
        RetailSupplier.objects.create(**modify_info)


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

    def query_repertory_goods_list(self,cid=0):
        sql = 'select * from goods right join repertory on goods.nid=repertory.goods_id'
        if cid > 0:
            sql += ' where goods.category_id={0}'.format(cid)
        result_db = Goods.objects.raw(sql)
        return result_db

    def query_goods_by_id(self, nid):
        result_db = Goods.objects.filter(nid=nid,delete_status=1).first()
        return result_db

    def query_goods_by_code(self,code):
        result_db = Goods.objects.filter(code=code, delete_status=1).first()
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


class RepertoryDB(object):
    """仓库库存"""

    def query_goods_by_gid(self,id):
        result_db = Repertory.objects.filter(goods_id=id).first()
        return result_db


    def multi_insert(self, id_list):
        for item in id_list:
            if self.is_exist(item):
                continue
            Repertory.objects.create(**{"goods_id":item})

    def multi_delete(self,id_list):
        Repertory.objects.filter(goods_id__in=id_list).delete()

    def is_exist(self,goods_id):
        is_exist = Repertory.objects.filter(goods_id=goods_id).first()
        return is_exist


class SupplierDB(object):
    """供应商管理"""
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

    def query_supplier_by_goods(self, gid):
        result_db = Supplier.objects.filter(goods_id=gid, delete_status=1).first()
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
    lunar_choice = ({"id": 0, "caption": "公历"}, {"id": 1, "caption": "农历"})

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
        ContactAttach.objects.filter(contact_id__in=id_list).filter().delete()

    def delete_contact_attachment(self,nid):
        ContactAttach.objects.filter(nid=nid).delete()


class MemoAttachDB(object):
    """备忘附件表"""
    def query_memo_attachment_list(self):
        result_db = MemoAttach.objects.filter().all()
        return result_db

    def query_memo_attachment(self, id):
        result_db = MemoAttach.objects.filter(memo_id=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            MemoAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            MemoAttach.objects.filter(nid=item['nid']).update(**item)

    def mutil_delete_memo_attachment(self, id_list):
        MemoAttach.objects.filter(nid__in=id_list).delete()

    def multi_delete_attach_by_linkman_id(self,id_list):
        MemoAttach.objects.filter(memo_id__in=id_list).filter().delete()

    def delete_memo_attachment(self,nid):
        MemoAttach.objects.filter(nid=nid).delete()


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


class WarehouseDB(object):
    """仓库"""

    def query_warehouse_list(self):
        result_db = Warehouse.objects.filter().all()
        return result_db

    def query_warehouse_by_id(self, id):
        result_db = Warehouse.objects.filter(nid=id).first()
        return result_db

    def insert_warehouse(self,modify_info):
        warehouse_sql = """insert into warehouse(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        warehouse_sql = warehouse_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(warehouse_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def update_warehouse(self,modify_info):
        Warehouse.objects.update(**modify_info)

class InventDB(object):
    "库存"

    def insert_invent(self, modify_info):
        invent_sql = """insert into inventory(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        invent_sql = invent_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(invent_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_goods_total_amount(self, gid):
        query_sql = """select sum(amount) as total_amount from inventory where goods_id={0}""".format(gid)
        cursor = connection.cursor()
        cursor.execute(query_sql)
        result_db = cursor.fetchone()
        return result_db

    def query_goods_total_amount_by_warehouse(self,gid,wid):
        query_sql = """select sum(amount) as total_amount from inventory where goods_id={0} and warehouse_id={1}""".format(gid,wid)
        cursor = connection.cursor()
        cursor.execute(query_sql)
        result_db = cursor.fetchone()
        return result_db

    def query_invent_list(self):
        result_db = Inventory.objects.filter(delete_status=1).all()
        return result_db

    def query_invent_by_id(self, nid):
        result_db = Inventory.objects.filter(nid=nid, delete_status=1).first()
        return result_db

    def query_invent_by_goods_warehouse(self, goods_id,warehouse_id):
        result_db = Inventory.objects.filter(goods_id=goods_id, warehouse_id=warehouse_id,delete_status=1).last()
        return result_db

    def query_invent_by_goods(self,goods_id):
        result_db = Inventory.objects.filter(goods_id=goods_id, delete_status=1).last()
        return result_db

    def query_invent_by_goods_list(self,goods_id):
        result_db = Inventory.objects.filter(goods_id=goods_id, delete_status=1).order_by("-date").all()
        return result_db

    def invent_update(self, modify):
        Inventory.objects.filter(nid=modify['nid'], delete_status=1).update(**modify)

    def mutil_update_purchase(self,id_list,pid):
        for item in id_list:
            Inventory.objects.filter(nid=item).update(purchase_id=pid)

    def multi_delete(self, id_list, delete_status):
        Inventory.objects.filter(nid__in=id_list).update(**delete_status)


class WareLocationDB(object):
    """城市"""

    def __init__(self):
        pass

    def query_location_list(self):
        result_db = WareLocation.objects.filter().all()
        return result_db

    def query_location_by_id(self, nid):
        result_db = WareLocation.objects.filter(nid=nid).first()
        return result_db

    def query_location_by_house(self, warehouse_id):
        result_db = WareLocation.objects.filter(warehouse_id=warehouse_id).all()
        return result_db

    def update_location(self, modify_info):
        is_exist = self.is_exist(modify_info["warehouse_id"], modify_info["location"])
        print(is_exist)
        if is_exist:
            raise Exception("该库位已存在")
        WareLocation.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_location(self, modify_info):
        is_exist = self.is_exist(modify_info["warehouse_id"], modify_info["location"])
        if is_exist:
            raise Exception("该库位已存在")
        WareLocation.objects.create(**modify_info)

    def is_exist(self, warehouse_id, location):
        result_db = WareLocation.objects.filter(warehouse_id=warehouse_id, location=location).first()
        return result_db


class InventoryAttachDB(object):
    """入库附件表"""
    def query_invent_attachment_list(self):
        result_db = InventoryAttach.objects.filter().all()
        return result_db

    def query_invent_attachment(self, id):
        result_db = InventoryAttach.objects.filter(inventory_id=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            InventoryAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            InventoryAttach.objects.filter(nid=item['nid']).update(**item)

    def mutil_delete_invent_attachment(self, id_list):
        InventoryAttach.objects.filter(nid__in=id_list).delete()

    def delete_invent_attachment(self, inventory_id):
        InventoryAttach.objects.filter(inventory_id=inventory_id).delete()


class PurchaseDB(object):
    "采购记录"

    def insert_purchase(self, modify_info):
        purchase_sql = """insert into purchase(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        purchase_sql = purchase_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(purchase_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_purchase_list(self):
        result_db = Purchase.objects.filter(delete_status=1).all()
        return result_db

    def query_purchase_by_id(self, nid):
        result_db = Purchase.objects.filter(nid=nid, delete_status=1).first()
        return result_db

    def query_purchase_by_goods(self,goods_id):
        result_db = Purchase.objects.filter(goods_id=goods_id, delete_status=1).last()
        return result_db

    def query_purchase_by_goods_list(self,goods_id):
        result_db = Purchase.objects.filter(goods_id=goods_id, delete_status=1).order_by("-date").all()
        return result_db

    def purchase_update(self, modify):
        Purchase.objects.filter(nid=modify['nid'], delete_status=1).update(**modify)

    def multi_delete(self, id_list, delete_status):
        Purchase.objects.filter(nid__in=id_list).update(**delete_status)


class PurchaseAttachDB(object):
    """采购凭证"""
    def query_purchase_attachment_list(self):
        result_db = PurchaseAttach.objects.filter().all()
        return result_db

    def query_purchase_attachment(self, id):
        result_db = PurchaseAttach.objects.filter(purchase_id=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            PurchaseAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            PurchaseAttach.objects.filter(nid=item['nid']).update(**item)

    def mutil_delete_purchase_attachment(self, id_list):
        PurchaseAttach.objects.filter(nid__in=id_list).delete()

    def delete_purchase_attachment(self, purchase_id):
        PurchaseAttach.objects.filter(purchase_id=purchase_id).delete()


class WastageGoodsDB(object):
    "损耗记录"
    def insert_wastage(self, modify_info):
        wastage_sql = """insert into wastage_goods(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        wastage_sql = wastage_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(wastage_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_wastage_list(self):
        result_db = WastageGoods.objects.filter().all()
        return result_db

    def query_wastage_by_id(self, nid):
        result_db = WastageGoods.objects.filter(nid=nid ).first()
        return result_db

    def query_wastage_by_goods_list(self,goods_id):
        result_db = WastageGoods.objects.filter(goods_id=goods_id).order_by("-date").all()
        return result_db

    def wastage_update(self, modify):
        WastageGoods.objects.filter(nid=modify['nid']).update(**modify)

    def multi_delete(self, id_list, delete_status):
        WastageGoods.objects.filter(nid__in=id_list).update(**delete_status)


class WastageAttachDB(object):
    """损耗凭证"""
    def query_wastage_attachment_list(self):
        result_db = WastageAttach.objects.filter().all()
        return result_db

    def query_wastage_attachment(self,id):
        result_db = WastageAttach.objects.filter(wastage_id=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            WastageAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            WastageAttach.objects.filter(nid=item['nid']).update(**item)

    def mutil_delete_wastage_attachment(self, id_list):
        WastageAttach.objects.filter(nid__in=id_list).delete()

    def delete_wastage_attachment(self, wastage_id):
        WastageAttach.objects.filter(wastage_id=wastage_id).delete()


class WastageSolverDB(object):
    """损耗处理人"""
    def mutil_insert(self,solver_list):
        for item in solver_list:
            WastageSolver.objects.get_or_create(**item)

    def query_wastage_solver(self,wid):
        result_db = WastageSolver.objects.filter(wid_id=wid).all()
        return result_db

    def delete_wastage_solver(self,wid):
        WastageSolver.objects.filter(wid_id= wid).delete()

    def mutil_delete(self,id_list):
        WastageSolver.objects.filter(sid_id__in=id_list).delete()


class LinkmanTitleDB(object):
    """职级表"""
    def query_job_title_list(self):
        result_db = LinkmanTitle.objects.filter().all()
        return result_db

    def query_job_title_by_id(self, id):
        result_db = LinkmanTitle.objects.filter(id=id).first()
        return result_db

    def update_job_title(self, modify_info):
        is_exist = LinkmanTitle.objects.filter(job_title=modify_info['job_title']).first()
        if is_exist:
            raise Exception("该职位名称已存在")
        LinkmanTitle.objects.filter(id=modify_info['id']).update(**modify_info)

    def insert_job_title(self, modify_info):
        is_exist = LinkmanTitle.objects.filter(job_title=modify_info['job_title']).first()
        if is_exist:
            raise Exception("该职位名称已存在")
        LinkmanTitle.objects.create(**modify_info)


supplier_db = SupplierDB()
supplier_photo_db = SupplierPhotoDB()
supplier_licence_db = SupplierLicenceDB()
supplier_attach_db = SupplierAttachDB()
supplier_contact_db = SupplierContactDB()
supplier_memo_db = SupplierMemoDB()
contact_attach_db = ContactAttachDB()
memo_attach_db = MemoAttachDB()
industry_db = IndustryDB()
supplier_category_db = SupplierCategoryDB()
goods_category_db = GoodsCategoryDB()
goods_unit_db = GoodsUnitDB()
goods_db = GoodsDB()
goods_price_db = GoodsPriceDB()
price_compare_db = PriceCompareDB()
retailer_db = RetailSupplierDB()
price_attach_db = PriceAttachDB()
goods_photo_db = GoodsPhotoDB()
goods_code_db = GoodsBarCodeDB()
goods_attach_db = GoodsAttachDB()
linkman_db = LinkmanDB()
linkman_photo_db = LinkmanPhotoDB()
linkman_card_db = LinkmanCardDB()
linkman_attach_db = LinkmanAttachDB()
warehouse_db = WarehouseDB()
ware_location_db = WareLocationDB()
invent_db = InventDB()
invent_attach_db = InventoryAttachDB()
purchase_db = PurchaseDB()
purchase_attach_db = PurchaseAttachDB()
repertory_db = RepertoryDB()
wastage_db = WastageGoodsDB()
wastage_attach_db = WastageAttachDB()
solver_db = WastageSolverDB()
linkman_title_db = LinkmanTitleDB()


