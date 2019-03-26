from django.db import connection
from .models import *


class StaffDB(object):
    """员工表"""
    gender_choice = ({"id": 0, "caption": "男"}, {"id": 1, "caption": "女"})
    lunar_choice = ({"id": 0, "caption": "公历"}, {"id": 1, "caption": "农历"})

    def insert_staff(self,modify_info):
        staff_sql = """insert into staff(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        staff_sql = staff_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(staff_sql, modify_info)
        sid = cursor.lastrowid
        return sid

    def query_staff_list(self):
        result_db = Staff.objects.filter(delete_status=1).all()
        return result_db

    def query_staff_by_id(self, sid):
        result_db = Staff.objects.filter(sid=sid).first()
        return result_db

    def query_staff_by_department_id(self, department_id):
        result_db = Staff.objects.filter(department=department_id,delete_status=1).all()
        return result_db

    def update_staff(self, modify):
        Staff.objects.filter(sid=modify['sid'],delete_status=1).update(**modify)

    def multi_delete(self, id_list, delete_status):
        Staff.objects.filter(sid__in=id_list).update(**delete_status)


class DepartmentDB(object):
    """部门表"""
    def query_department_list(self):
        result_db = Department.objects.filter().all()
        return result_db

    def query_department_by_id(self,id):
        result_db = Department.objects.filter(id=id).first()
        return result_db

    def update_deaprtment(self, modify_info):
        is_exist = Department.objects.filter(department=modify_info['department']).first()
        if is_exist:
            raise Exception("该部门名称已存在")
        Department.objects.filter(id=modify_info['id']).update(**modify_info)

    def insert_department(self, modify_info):
        is_exist = Department.objects.filter(department=modify_info['department']).first()
        if is_exist:
            raise Exception("该部门名称已存在")
        Department.objects.create(**modify_info)


class CompanyDB(object):
    """公司表"""
    def query_company_list(self):
        result_db = Company.objects.filter().all()
        return result_db

    def query_company_by_id(self,id):
        result_db = Company.objects.filter(id=id).first()
        return result_db

    def query_company_by_c_id(self, sid):
        result_db = Company.objects.filter(sid=sid).all().order_by("-sid")
        return result_db

    def update_company(self, modify_info):
        is_exist = Company.objects.filter(company=modify_info['company']).first()
        if is_exist:
            raise Exception("该公司名称已存在")
        Company.objects.filter(id=modify_info['id']).update(**modify_info)

    def insert_company(self, modify_info):
        is_exist = Company.objects.filter(company=modify_info['company']).first()
        if is_exist:
            raise Exception("该公司名称已存在")
        Company.objects.create(**modify_info)


class ProjectDB(object):
    """项目表"""
    def query_project_list(self):
        result_db = Project.objects.filter().all()
        return result_db

    def query_project_by_id(self, id):
        result_db = Project.objects.filter(id=id).first()
        return result_db

    def update_project(self, modify_info):
        is_exist = Project.objects.filter(project=modify_info['project']).first()
        if is_exist:
            raise Exception("该项目名称已存在")
        Project.objects.filter(id=modify_info['id']).update(**modify_info)

    def insert_project(self, modify_info):
        is_exist = Project.objects.filter(project=modify_info['project']).first()
        if is_exist:
            raise Exception("该项目名称已存在")
        Project.objects.create(**modify_info)


class JobRankDB(object):
    """职级表"""

    def query_job_rank_list(self):
        result_db = JobRank.objects.filter().all()
        return result_db

    def query_job_rank_by_id(self, id):
        result_db = JobRank.objects.filter(id=id).first()
        return result_db

    def update_job_rank(self, modify_info):
        is_exist = JobRank.objects.filter(rank=modify_info['rank']).first()
        if is_exist:
            raise Exception("该项目名称已存在")
        JobRank.objects.filter(id=modify_info['id']).update(**modify_info)

    def insert_job_rank(self, modify_info):
        is_exist = JobRank.objects.filter(rank=modify_info['rank']).first()
        if is_exist:
            raise Exception("该项目名称已存在")
        JobRank.objects.create(**modify_info)


class JobTitleDB(object):
    """职级表"""

    def query_job_title_list(self):
        result_db = JobTitle.objects.filter().all()
        return result_db

    def query_job_title_by_id(self, id):
        result_db = JobTitle.objects.filter(id=id).first()
        return result_db

    def update_job_title(self, modify_info):
        is_exist = JobTitle.objects.filter(job_title=modify_info['job_title']).first()
        if is_exist:
            raise Exception("该职位名称已存在")
        JobTitle.objects.filter(id=modify_info['id']).update(**modify_info)

    def insert_job_title(self, modify_info):
        is_exist = JobTitle.objects.filter(job_title=modify_info['job_title']).first()
        if is_exist:
            raise Exception("该职位名称已存在")
        JobTitle.objects.create(**modify_info)

class S_Project(object):

    def project_list(self):
        project_db = Select_Project.objects.filter().all()
        return project_db

    def query_s_title_by_id(self, id):
        result_db = Select_Project.objects.filter(id=id).first()
        return result_db

    def update_select_project_title(self, modify_info):
        is_exist = Select_Project.objects.filter(name=modify_info['name']).first()
        if is_exist:
            raise Exception("该名称已存在")
        Select_Project.objects.filter(id=modify_info['id']).update(**modify_info)

    def insert_select_project_title(self, modify_info):
        is_exist = Select_Project.objects.filter(name=modify_info['name']).first()
        if is_exist:
            raise Exception("该名称已存在")
        Select_Project.objects.create(**modify_info)

    def multi_delete(self,id_list):
        Select_Project.objects.filter(id__in=id_list).delete()


class ReasonsPeopleDB(object):
    """工作交接人"""

    def people_db (self):
        people_db = ReasonsPeople.objects.filter().all()
        return people_db

    def query_p_title_by_id(self, id):
        result_db = ReasonsPeople.objects.filter(id=id).first()
        return result_db

class ReasonsCauseDB(object):
    """离职的原因"""

    def reasons_cause_db(self):
        cause_db = ReasonsCause.objects.filter().all()
        return cause_db

    def query_cause_by_id(self, id):
        result_db = ReasonsCause.objects.filter(id=id).first()
        return result_db

    def update_cause_title(self, modify_info):
        is_exist = ReasonsCause.objects.filter(cause=modify_info['cause']).first()
        if is_exist:
            raise Exception("该名称已存在")
        ReasonsCause.objects.filter(id=modify_info['id']).update(**modify_info)

    def insert_cause_title(self, modify_info):
        is_exist = ReasonsCause.objects.filter(cause=modify_info['cause']).first()
        if is_exist:
            raise Exception("该名称已存在")
        ReasonsCause.objects.create(**modify_info)

    def mulit_delete(self,id_list):
        ReasonsCause.objects.filter(id__in=id_list).delete()


class StaffLifePhotoDB(object):
    """人事生活照"""

    def insert_life_photo(self, modify):
        StaffLifePhoto.objects.create(**modify)

    def query_life_photo_by_sid(self,sid):
        result_db = StaffLifePhoto.objects.filter(sid_id=sid).first()
        return result_db

    def update_photo(self, modify):
        StaffLifePhoto.objects.filter(sid_id=modify["sid_id"]).update(**modify)

    def delete_photo_by_sid(self, sid):
       StaffLifePhoto.objects.filter(sid_id=sid).delete()


class StaffAttachDB(object):
    """任务附件表"""
    def query_staff_attachment_list(self):
        result_db = StaffAttach.objects.filter().all()
        return result_db

    def query_staff_attachment_by_sid(self, sid):
        result_db = StaffAttach.objects.filter(sid_id=sid).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            StaffAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            StaffAttach.objects.filter(said=item['said']).update(**item)

    def mutil_delete_task_attachment(self, id_list):
        StaffAttach.objects.filter(said__in=id_list).delete()

    def multi_delete_attach_by_sid(self,id_list):
        StaffAttach.objects.filter(sid_id__in=id_list).filter().delete()

    def delete_task_attachment(self,said):
        StaffAttach.objects.filter(said=said).delete()

class PerforManceygDB(object):
    """就职表现表"""
    def insert_edit1(self, modify_info):
        perfor_sql = """insert into performanceyg(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        perfor_sql = perfor_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(perfor_sql, modify_info)
        nid = cursor.lastrowid
        return nid

    def query_perfor_by_id(self, sid):
        result_db = Performanceyg.objects.filter(nid=sid).first()
        return  result_db

    def update_perfor(self, modify):
        Performanceyg.objects.filter(sid=modify['sid']).update(**modify)

    def query_perfor_by_p_id(self, id):
            result_db = Performanceyg.objects.filter(sid_id=id, ).all().order_by("-nid")
            return result_db

    def multi_delete(self, id_list):
        Performanceyg.objects.filter(nid__in=id_list).delete()


class PerforygAttachDB(object):
    def query_perfor_attachment(self, id):
        result_db = PerforygmanceAttach.objects.filter(sid=id).all()
        return result_db

    def query_perfor_attachment_by_sid(self, sid):
        result_db = PerforygmanceAttach.objects.filter(sid_id=sid).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            PerforygmanceAttach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            PerforygmanceAttach.objects.filter(said=item['said']).update(**item)

    def mutil_delete_task_attachment(self, id_list):
        PerforygmanceAttach.objects.filter(said__in=id_list).delete()

    def multi_delete_attach_by_edit1_id(self, id_list):
        PerforygmanceAttach.objects.filter(edit1_id__in=id_list).filter().delete()

class LaborContractDB(object):
    """工作合同表"""
    def insert_edit2(self, modify_info):
        Labor_sql = """insert into labor_contract(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        staff_sql = Labor_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(staff_sql, modify_info)
        sid = cursor.lastrowid
        return sid

    def query_labor_by_id(self, nid):
        result_db = LaborContract.objects.filter(nid=nid).first()
        return result_db

    def query_labor_by_c_id(self, sid):
        result_db = LaborContract.objects.filter(sid=sid).all().order_by("-sid")
        return result_db

    def multi_delete(self, id_list):
        LaborContract.objects.filter(nid__in=id_list).delete()


class LaborAttachDB(object):
    def query_labor_attachment(self, id):
        result_db = Labor_Contract_Attach.objects.filter(sid=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            Labor_Contract_Attach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            Labor_Contract_Attach.filter(said=item['said']).update(**item)

    def mutil_delete_task_attachment(self, id_list):
        Labor_Contract_Attach.objects.filter(said__in=id_list).delete()

    def multi_delete_attach_by_edit2_id(self, id_list):
        Labor_Contract_Attach.objects.filter(edit1_id__in=id_list).filter().delete()

class ArticleDB(object):
    def article_list(self):
        article_db = Article.objects.filter().all()
        return article_db

    def query_a_title_by_id(self, id):
        result_db = Article.objects.filter(id=id).first()
        return result_db

    def update_article_title(self, modify_info):
        is_exist = Article.objects.filter(name=modify_info['name']).first()
        if is_exist:
            raise Exception("该职位名称已存在")
        Article.objects.filter(id=modify_info['id']).update(**modify_info)

    def insert_article_title(self, modify_info):
        is_exist = Article.objects.filter(name=modify_info['name']).first()
        if is_exist:
            raise Exception("该职位名称已存在")
        Article.objects.create(**modify_info)

class ReasonsLeaveDB(object):
    def insert_edit3(self, modify_info):
        reasons_sql = """insert into reasonsleave(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        staff_sql = reasons_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(staff_sql, modify_info)
        sid = cursor.lastrowid
        return sid

    def query_reasons_by_id(self, nid):
        result_db = ReasonsLeave.objects.filter(nid=nid).first()
        return result_db

    def query_reasons_by_l_id(self, nid):
        result_db = ReasonsLeave.objects.filter(nid=nid).all().order_by("-nid")
        return result_db

    def multi_delete(self, id_list):
        ReasonsLeave.objects.filter(nid__in=id_list).delete()

class ReasonsAttachDB(object):
    def query_reasons_attachment(self, id):
        result_db = Reasonsleave_Attach.objects.filter(sid=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            Reasonsleave_Attach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            Reasonsleave_Attach.objects.filter(said=item['said']).update(**item)

    def mutil_delete_task_attachment(self, id_list):
        Reasonsleave_Attach.objects.filter(said__in=id_list).delete()

    def multi_delete_attach_by_edit3_id(self, id_list):
        Reasonsleave_Attach.objects.filter(edit1_id__in=id_list).filter().delete()

class SocialSecurityDB(object):
    def insert_edit4(self, modify_info):
        social_sql = """insert into social_security(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        staff_sql = social_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(staff_sql, modify_info)
        sid = cursor.lastrowid
        return sid

    def query_social_by_id(self, nid):
        result_db = SocialSecurity.objects.filter(nid=nid).first()
        return result_db

    def query_social_by_s_id(self, sid):
        result_db = SocialSecurity.objects.filter(sid=sid).all().order_by("-nid")
        return result_db

    def multi_delete(self, id_list):
        SocialSecurity.objects.filter(nid__in=id_list).delete()


class SocialAttachDB(object):
    def query_social_attachment(self, id):
        result_db = Social_Attach.objects.filter(sid=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            Social_Attach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            Social_Attach.objects.filter(said=item['said']).update(**item)

    def mutil_delete_task_attachment(self, id_list):
        Social_Attach.objects.filter(said__in=id_list).delete()

    def multi_delete_attach_by_edit4_id(self, id_list):
        Social_Attach.objects.filter(edit1_id__in=id_list).filter().delete()

class SuppliesDB(object):
    def insert_edit5(self, modify_info):
        supp_sql = """insert into supplies(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        staff_sql = supp_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(staff_sql, modify_info)
        sid = cursor.lastrowid
        return sid

    def query_supp_by_id(self, nid):
        result_db = Supplies.objects.filter(nid=nid).first()
        return result_db

    def query_supp_by_s_id(self, sid):
        result_db = Supplies.objects.filter(sid=sid).all().order_by("-sid")
        return result_db

    def multi_delete(self, id_list):
        Supplies.objects.filter(nid__in=id_list).delete()


class SuppliesAttachDB(object):
    def query_supp_attachment(self, id):
        result_db = Supplies_Attach.objects.filter(sid=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            Supplies_Attach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            Supplies_Attach.objects.filter(said=item['said']).update(**item)

    def mutil_delete_task_attachment(self, id_list):
        Supplies_Attach.objects.filter(said__in=id_list).delete()

    def multi_delete_attach_by_edit5_id(self, id_list):
        Supplies_Attach.objects.filter(edit1_id__in=id_list).filter().delete()


class SuppliesReturnDB(object):
    def insert_edit6(self, modify_info):
        supp_sql = """insert into supplies_return(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        staff_sql = supp_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(staff_sql, modify_info)
        sid = cursor.lastrowid
        return sid

    def query_supp_by_id(self, nid):
        result_db = Supplies_Return.objects.filter(nid=nid).first()
        return result_db

    def query_supp_by_s_id(self, sid):
        result_db = Supplies_Return.objects.filter(sid=sid).all().order_by("-sid")
        return result_db

    def multi_delete(self, id_list):
        Supplies_Return.objects.filter(nid__in=id_list).delete()

class SuppliesReturnAttachDB(object):
    def query_supp_attachment(self, id):
        result_db = Supplies_Return_Attach.objects.filter(sid=id).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            Supplies_Return_Attach.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            Supplies_Return_Attach.objects.filter(said=item['said']).update(**item)

    def mutil_delete_task_attachment(self, id_list):
        Supplies_Return_Attach.objects.filter(said__in=id_list).delete()

    def multi_delete_attach_by_edit5_id(self, id_list):
        Supplies_Return_Attach.objects.filter(edit1_id__in=id_list).filter().delete()

department_db = DepartmentDB()
company_db = CompanyDB()
project_db = ProjectDB()
job_rank_db = JobRankDB()
job_title_db = JobTitleDB()
select_project_db = S_Project()
staff_db = StaffDB()
staff_life_photo_db = StaffLifePhotoDB()
staff_attach_db = StaffAttachDB()
performanceyg_db = PerforManceygDB()
perforygattach_db = PerforygAttachDB()
laborcontract_db = LaborContractDB()
laborattach_db = LaborAttachDB()
article1_db = ArticleDB()
rea_people_db = ReasonsPeopleDB()
reasonsleave_db = ReasonsLeaveDB()
reasonsattach_db = ReasonsAttachDB()
socialsecurity_db = SocialSecurityDB()
socialattach_db = SocialAttachDB()
supplies_db = SuppliesDB()
suppliesattach_db = SuppliesAttachDB()
suppliesreturn_db = SuppliesReturnDB()
suppliesreturnattach_db = SuppliesReturnAttachDB()
reasonscause_db = ReasonsCauseDB()


