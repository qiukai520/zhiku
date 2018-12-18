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

    def multi_delete(self, id_list):
        CustomerInfo.objects.filter(nid__in=id_list).delete()



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



class CustomerLinkmanDB(object):
    """联系人表"""
    gender_choice = ({"id": 0, "caption": "男"}, {"id": 1, "caption": "女"})
    marriage_choice = ({"id": 0, "caption": "未婚"}, {"id": 1, "caption": "已婚"})
    lunar_choice = ({"id": 0, "caption": "公历"}, {"id": 1, "caption": "农历"})

    def insert_linkman(self, modify_info):
        linkman_sql = """insert into customer_linkman(%s) value(%s);"""
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
        result_db = CustomerLinkman.objects.filter().all()
        return result_db

    def query_linkman_by_id(self, nid):
        result_db = CustomerLinkman.objects.filter(nid=nid).first()
        return result_db

    def query_linkman_by_customer_id(self,id):
        result_db = CustomerLinkman.objects.filter(customer_id=id,).all().order_by("-nid")
        return result_db

    def update_linkman(self, modify):
        CustomerLinkman.objects.filter(nid=modify['nid'],).update(**modify)

    def multi_delete(self, id_list, delete_status):
        CustomerLinkman.objects.filter(nid__in=id_list).update(**delete_status)


class CustomerLinkmanPhotoDB(object):
    """供应商图片"""

    def insert_photo(self, modify):
        CustomerLinkmanPhoto.objects.create(**modify)

    def query_linkman_photo(self,id):
        result_db = CustomerLinkmanPhoto.objects.filter(linkman_id=id).first()
        return result_db

    def update_photo(self, modify):
        CustomerLinkmanPhoto.objects.filter(linkman_id=modify["linkman_id"]).update(**modify)

    def delete_photo_by_linkman_id(self, id):
        CustomerLinkmanPhoto.objects.filter(linkman_id=id).delete()


class CustomerLinkmanCardDB(object):
    """联系人卡片"""

    def insert_photo(self, modify):
        CustomerLinkmanCard.objects.create(**modify)

    def query_linkman_card(self,id):
        result_db = CustomerLinkmanCard.objects.filter(linkman_id=id).first()
        return result_db

    def update_card(self, modify):
        CustomerLinkmanCard.objects.filter(linkman_id=modify["linkman_id"]).update(**modify)

    def delete_card_by_card_id(self,id):
        CustomerLinkmanCard.objects.filter(linkman_id=id).delete()


class CustomerLinkmanAttachDB(object):
    """联系人附件表"""
    def query_linkman_attachment_list(self):
        result_db = CustomerLinkmanAttach.objects.filter().all()
        return result_db

    def query_linkman_attachment(self,id):
        result_db = CustomerLinkmanAttach.objects.filter(linkman_id=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            CustomerLinkmanAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            CustomerLinkmanAttach.objects.filter(nid=item['nid']).update(**item)

    def mutil_delete_linkman_attachment(self, id_list):
        CustomerLinkmanAttach.objects.filter(nid__in=id_list).delete()

    def multi_delete_attach_by_linkman_id(self,id_list):
        CustomerLinkmanAttach.objects.filter(linkman_id__in=id_list).filter().delete()

    def delete_linkman_attachment(self,nid):
        CustomerLinkmanAttach.objects.filter(nid=nid).delete()


class CustomerMemoDB(object):
    """供应商备忘"""
    def insert_memo(self, modify_info):
        memo_sql = """insert into customer_memo(%s) value(%s);"""
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
        result_db = CustomerMemo.objects.filter().all()
        return result_db

    def query_memo_by_id(self, nid):
        result_db = CustomerMemo.objects.filter(nid=nid).first()
        return result_db

    def query_memo_by_customer_id(self, sid):
        result_db = CustomerMemo.objects.filter(customer_id=sid).all().order_by("-nid")
        return result_db

    def update_memo(self, modify_info):
        CustomerMemo.objects.filter(nid=modify_info['nid']).update(**modify_info)


class CustomerMemoAttachDB(object):
    """备忘附件表"""
    def query_memo_attachment_list(self):
        result_db = CustomerMemoAttach.objects.filter().all()
        return result_db

    def query_memo_attachment(self, id):
        result_db = CustomerMemoAttach.objects.filter(memo_id=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            CustomerMemoAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            CustomerMemoAttach.objects.filter(nid=item['nid']).update(**item)

    def mutil_delete_memo_attachment(self, id_list):
        CustomerMemoAttach.objects.filter(nid__in=id_list).delete()

    def multi_delete_attach_by_memo_id(self,id_list):
        CustomerMemoAttach.objects.filter(memo_id__in=id_list).filter().delete()

    def delete_memo_attachment(self,nid):
        CustomerMemoAttach.objects.filter(nid=nid).delete()


class CustomerContactDB(object):
    """客户来往"""
    category= ({"id": 0, "caption": "收入"}, {"id": 1, "caption": "支出"})

    def insert_contact(self, modify_info):
        contact_sql = """insert into customer_contact(%s) value(%s);"""
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
        result_db = CustomerContact.objects.all()
        return result_db

    def query_contact_by_id(self, nid):
        result_db = CustomerContact.objects.filter(nid=nid).first()
        return result_db

    def query_contact_by_customer(self,customer_id):
        result_db = CustomerContact.objects.filter(customer_id=customer_id).all()
        return result_db

    def update_contact(self, modify):
        CustomerContact.objects.filter(nid=modify['nid']).update(**modify)

    def multi_delete(self, id_list, delete_status):
        CustomerContact.objects.filter(nid__in=id_list).update(**delete_status)


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


class CustomerFollowDB(object):
    """客户跟进记录"""

    def insert_follow(self, modify_info):
        follow_sql = """insert into customer_follow(%s) value(%s);"""
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
        result_db = CustomerFollow.objects.filter().all()
        return result_db

    def query_follow_by_id(self, nid):
        result_db = CustomerFollow.objects.filter(nid=nid).first()
        return result_db

    def query_follow_by_customer_id(self, sid):
        result_db = CustomerFollow.objects.filter(customer_id=sid).all().order_by("-nid")
        return result_db

    def update_follow(self, modify):
        CustomerFollow.objects.filter(nid=modify['nid']).update(**modify)

    def multi_delete(self, id_list):
        CustomerFollow.objects.filter(nid__in=id_list).delete()


class FollowAttachDB(object):
    """跟踪附件表"""
    def query_follow_attachment_list(self):
        result_db = CustomerFollowAttach.objects.filter().all()
        return result_db

    def query_follow_attachment(self, id):
        result_db = CustomerFollowAttach.objects.filter(follow_id=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            CustomerFollowAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            CustomerFollowAttach.objects.filter(nid=item['nid']).update(**item)

    def mutil_delete_follow_attachment(self, id_list):
        CustomerFollowAttach.objects.filter(nid__in=id_list).delete()

    def multi_delete_attach_by_follow_id(self,id_list):
        CustomerFollowAttach.objects.filter(follow_id__in=id_list).filter().delete()

    def delete_attachment(self,nid):
        CustomerFollowAttach.objects.filter(nid=nid).delete()


class FollowWayDB(object):
    """客户跟进方式"""
    def query_way_list(self):
        result_db = FollowWay.objects.filter().all()
        return result_db

    def query_way_by_id(self, nid):
        result_db = FollowWay.objects.filter(nid=nid).first()
        return result_db

    def update_way(self, modify_info):
        is_exist = FollowWay.objects.filter(code=modify_info['code']).first()
        if is_exist:
            raise Exception("该算法编号已存在")
        FollowWay.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_way(self, modify_info):
        is_exist = FollowWay.objects.filter(code=modify_info['code']).first()
        if is_exist:
            raise Exception("该算法编号已存在")
        FollowWay.objects.create(**modify_info)


class FollowContactDB(object):
    """联络方式"""
    def query_contact_list(self):
        result_db = FollowContact.objects.filter().all()
        return result_db

    def query_contact_by_id(self, nid):
        result_db = FollowContact.objects.filter(nid=nid).first()
        return result_db

    def update_contact(self, modify_info):
        is_exist = FollowContact.objects.filter(code=modify_info['code']).first()
        if is_exist:
            raise Exception("{0}算法编号已存在".format(modify_info['code']))
        FollowContact.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_contact(self, modify_info):
        is_exist = FollowContact.objects.filter(code=modify_info['code']).first()
        if is_exist:
            raise Exception("{0}该算法编号已存在".format(modify_info['code']))
        FollowContact.objects.create(**modify_info)


class CustomerPurposeDB(object):
    """客户跟进方式"""
    def query_purpose_list(self):
        result_db = CustomerPurpose.objects.filter().all()
        return result_db

    def query_purpose_by_id(self, nid):
        result_db = CustomerPurpose.objects.filter(nid=nid).first()
        return result_db

    def update_purpose(self, modify_info):
        is_exist = CustomerPurpose.objects.filter(code=modify_info['code']).first()
        if is_exist:
            raise Exception("{0}算法编号已存在".format(modify_info['code']))
        CustomerPurpose.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_purpose(self, modify_info):
        is_exist = CustomerPurpose.objects.filter(code=modify_info['code']).first()
        if is_exist:
            raise Exception("{0}算法编号已存在".format(modify_info['code']))
        CustomerPurpose.objects.create(**modify_info)


class FollowResultDB(object):
    """需求意向"""
    def query_result_list(self):
        result_db = FollowResult.objects.filter().all()
        return result_db

    def query_result_by_id(self, nid):
        result_db = FollowResult.objects.filter(nid=nid).first()
        return result_db

    def update_result(self, modify_info):
        is_exist = FollowResult.objects.filter(code=modify_info['code']).first()
        if is_exist:
            raise Exception("{0}算法编号已存在".format(modify_info['code']))
        FollowResult.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_way(self, modify_info):
        is_exist = FollowWay.objects.filter(code=modify_info['code']).first()
        if is_exist:
            raise Exception("{0}算法编号已存在".format(modify_info['code']))
        FollowResult.objects.create(**modify_info)


class LinkmanTitleDB(object):
    """职级表"""
    def query_job_title_list(self):
        result_db =  LinkmanTitle.objects.filter().all()
        return result_db

    def query_job_title_by_id(self, id):
        result_db =  LinkmanTitle.objects.filter(id=id).first()
        return result_db

    def update_job_title(self, modify_info):
        is_exist =  LinkmanTitle.objects.filter(job_title=modify_info['job_title']).first()
        if is_exist:
            raise Exception("该职位名称已存在")
        LinkmanTitle.objects.filter(id=modify_info['id']).update(**modify_info)

    def insert_job_title(self, modify_info):
        is_exist = LinkmanTitle.objects.filter(job_title=modify_info['job_title']).first()
        if is_exist:
            raise Exception("该职位名称已存在")
        LinkmanTitle.objects.create(**modify_info)


customer_db = CustomerDB()
customer_category_db = CustomerCategoryDB()
customer_attach_db = CustomerAttachDB()
customer_licence_db = CustomerLicenceDB()
customer_photo_db = CustomerPhotoDB()
c_linkman_db = CustomerLinkmanDB()
c_linkman_photo_db = CustomerLinkmanPhotoDB()
c_linkman_card_db = CustomerLinkmanCardDB()
c_linkman_attach_db = CustomerLinkmanAttachDB()
c_memo_db = CustomerMemoDB()
c_memo_attach_db = CustomerMemoAttachDB()
c_contact_db=CustomerContactDB()
c_contact_attach_db = ContactAttachDB()
c_follow_db = CustomerFollowDB()
follow_way_db = FollowWayDB()
follow_contact_db = FollowContactDB()
follow_result_db = FollowResultDB()
c_follow_attach_db = FollowAttachDB()
customer_purpose_db = CustomerPurposeDB()

linkman_title_db = LinkmanTitleDB()
