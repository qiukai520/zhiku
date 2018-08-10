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


department_db = DepartmentDB()
staff_db = StaffDB()