from .models import *

class StaffDB(object):
    """员工表"""
    sex = ({"id": 0, "caption": "男"}, {"id": 1, "caption": "女"})

    def query_staff_list(self):
        result_db = Staff.objects.filter().all()
        return result_db

    def query_staff_by_id(self, sid):
        result_db = Staff.objects.filter(sid=sid).first()
        return result_db

    def query_staff_by_department_id(self, department_id):
        result_db = Staff.objects.filter(department=department_id).all()
        return result_db


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
    """部门表"""
    def query_company_list(self):
        result_db = Company.objects.filter().all()
        return result_db

    def query_company_by_id(self,id):
        result_db = Company.objects.filter(id=id).first()
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
        is_exist = JobRank.objects.filter(job_rank=modify_info['job_rank']).first()
        if is_exist:
            raise Exception("该项目名称已存在")
        JobRank.objects.filter(id=modify_info['id']).update(**modify_info)

    def insert_job_rank(self, modify_info):
        is_exist = JobRank.objects.filter(job_rank=modify_info['job_rank']).first()
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
            raise Exception("该项目名称已存在")
        JobTitle.objects.filter(id=modify_info['id']).update(**modify_info)

    def insert_job_title(self, modify_info):
        is_exist = JobTitle.objects.filter(job_title=modify_info['job_title']).first()
        if is_exist:
            raise Exception("该项目名称已存在")
        JobTitle.objects.create(**modify_info)


department_db = DepartmentDB()
company_db = CompanyDB()
project_db = ProjectDB()
job_rank_db = JobRankDB()
job_title_db = JobTitleDB()
staff_db = StaffDB()