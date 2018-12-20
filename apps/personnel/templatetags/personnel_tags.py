from django import template
from ..server import *
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def change_to_sex(gender):
    gender_list = staff_db.gender_choice
    for item in gender_list:
        if int(item["id"]) == gender:
            return item["caption"]

@register.simple_tag
def change_to_lunar(lunar):
    lunar_choice = staff_db.lunar_choice
    for item in lunar_choice:
        if int(item["id"]) == lunar:
            return item["caption"]

@register.simple_tag
def change_to_company(id):
    if id:
        company_obj = company_db.query_company_by_id(id)
        if company_obj:
            return company_obj.company
    return "空"

@register.simple_tag
def change_to_project(id):
    if id:
        project_obj = project_db.query_project_by_id(id)
        if project_obj:
            return project_obj.project
    return "空"


@register.simple_tag
def change_to_department(id):
    if id:
        department_obj = department_db.query_department_by_id(id)
        if department_obj:
            return department_obj.department
    return "空"

@register.simple_tag
def change_to_job_rank(id):
    if id:
        job_rank_obj = job_rank_db.query_job_rank_by_id(id)
        if job_rank_obj:
            return job_rank_obj.rank
    return "空"

@register.simple_tag
def change_to_job_title(id):
    if id:
        job_title_obj = job_title_db.query_job_title_by_id(id)
        if job_title_obj:
            return job_title_obj.job_title
    return "空"

@register.simple_tag
def build_company_ele():
    """构建公司下拉框"""
    company_list = company_db.query_company_list()
    eles = ""
    for item in company_list:
        ele = """<option value={0}>{1}</option>""".format(item.id, item.company)
        eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_project_ele():
    """构建项目下拉框"""
    project_list = project_db.query_project_list()
    eles = ""
    for item in project_list:
        ele = """<option value={0}>{1}</option>""".format(item.id, item.project)
        eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_department_ele(selected=0):
    """构建部门下拉框"""
    department_list = department_db.query_department_list()
    eles = ""
    for item in department_list:
        if item.id == selected:
            ele = """<option  selected="selected" value={0}>{1}</option>""".format(item.id, item.department)
        else:
            ele = """<option value={0}>{1}</option>""".format(item.id, item.department)
        eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_staff_ele(selected=0):
    """构建员工拉框"""
    staff_list = staff_db.query_staff_list()
    eles = ""
    for item in staff_list:
        if item.sid == selected:
            ele = """<option  selected="selected" value={0}>{1}</option>""".format(item.sid, item.name)
        else:
            ele = """<option value={0}>{1}</option>""".format(item.sid, item.name)
        eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_job_rank_ele():
    """构建职级下拉框"""
    job_rank_list =job_rank_db.query_job_rank_list()
    eles = ""
    for item in job_rank_list:
        ele = """<option value={0}>{1}</option>""".format(item.id, item.rank)
        eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_job_title_ele():
    """构建职称下拉框"""
    job_title_list =job_title_db.query_job_title_list()
    eles = ""
    for item in job_title_list:
        ele = """<option value={0}>{1}</option>""".format(item.id, item.job_title)
        eles += ele
    return mark_safe(eles)