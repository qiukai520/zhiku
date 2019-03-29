from django import template
from ..server import *
from django.utils.safestring import mark_safe
from revenue.server import *
from assets.server import *


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
def change_to_s_project(id):
    if id:
        s_title_obj = select_project_db.query_s_title_by_id(id)
        if s_title_obj:
            return s_title_obj.name
    return "空"

@register.simple_tag
def change_to_a_article(id):
    if id:
        a_title_obj = article1_db.query_a_title_by_id(id)
        if a_title_obj:
            return a_title_obj.name
    return "空"

@register.simple_tag
def change_to_supplies(id):
    if id:
        a_title_obj = assets_db.query_assets_by_id(id)
        if a_title_obj:
            return a_title_obj.name
    return "空"


# 收入支出
@register.simple_tag
def change_to_incomeclassify(id):
    if id:
        classify_obj = incomeclassify_db.query_classify_by_id(id)
        if classify_obj:
            return classify_obj.name
    return "空"

@register.simple_tag
def change_to_associates(id):
    if id:
        a_title_obj = associates_db.query_associates_by_id(id)
        if a_title_obj:
            return a_title_obj.name
    return "空"

@register.simple_tag
def change_to_approver2(id):
    if id:
        a_title_obj = approver2_db.query_approver2_by_id(id)
        if a_title_obj:
            return a_title_obj.name
    return "空"


# 资产管理
@register.simple_tag
def change_to_assets_classify(id):
    if id:
        a_title_obj = assetsclassify_db.query_classify_by_id(id)
        if a_title_obj:
            return a_title_obj.name
    return "空"

@register.simple_tag
def change_to_save_coordinate(id):
    if id:
        s_title_obj = save_coordinate_db.query_coordinate_by_id(id)
        if s_title_obj:
            return s_title_obj.name
    return "空"

@register.simple_tag
def change_to_procurement(id):
    if id:
        p_title_obj = procurement_db.query_procurement_by_id(id)
        if p_title_obj:
            return p_title_obj.name
    return "空"

@register.simple_tag
def change_to_username(id):
    if id:
        u_title_obj = username_db.query_username_by_id(id)
        if u_title_obj:
            return u_title_obj.name
    return "空"

@register.simple_tag
def change_to_assets_status(id):
    if id:
        a_title_obj = assets_status_db.query_assets_status_by_id(id)
        if a_title_obj:
            return a_title_obj.name
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


# 资产管理
@register.simple_tag
def build_assets_classify_ele():
    """构建分类下拉框"""
    classify_list = assetsclassify_db.query_classify_list()
    eles = ""
    for item in classify_list:
        ele = """<option value={0}>{1}</option>""".format(item.id, item.name)
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_purcurement_name_ele():
    """构建采购人下拉框"""
    name_list = procurement_db.query_procurement_list()
    eles = ""
    for item in name_list:
        ele = """<option value={0}>{1}</option>""".format(item.id, item.name)
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_user_name_ele():
    """构建使用人下拉框"""
    name_list = username_db.query_username_list()
    eles = ""
    for item in name_list:
        ele = """<option value={0}>{1}</option>""".format(item.id, item.name)
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_assets_status_ele():
    """构建资产状态下拉框"""
    name_list = assets_status_db.query_assets_status_list()
    eles = ""
    for item in name_list:
        ele = """<option value={0}>{1}</option>""".format(item.id, item.name)
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_save_coordinate_ele():
    """构建存档坐标下拉框"""
    name_list = save_coordinate_db.query_coordinate_list()
    eles = ""
    for item in name_list:
        ele = """<option value={0}>{1}</option>""".format(item.id, item.name)
        eles += ele
    return mark_safe(eles)


# 收支管理
@register.simple_tag
def build_classify_ele(selected=0):
    """构建收入分类下拉框"""
    classify_list = incomeclassify_db.query_classify_list()
    eles = ""
    for item in classify_list:
        if item.id == selected:
            ele = """<option  selected="selected" value={0}>{1}</option>""".format(item.id, item.name)
        else:
            ele = """<option value={0}>{1}</option>""".format(item.id, item.name)
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_associates_ele():
    """构建关联人下拉框"""
    associates_list = associates_db.query_associates_list()
    eles = ""
    for item in associates_list:
        ele = """<option value={0}>{1}</option>""".format(item.id, item.name)
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_approver2_ele():
    """构建审批人下拉框"""
    approver2_list =approver2_db.query_approver2_list()
    eles = ""
    for item in approver2_list:
        ele = """<option value={0}>{1}</option>""".format(item.id, item.name)
        eles += ele
    return mark_safe(eles)



@register.simple_tag
def build_staff_search_ele(dpid=0, sid=0):
    """构建员工下拉框"""
    if dpid != ''and 0:
         #根据部门获取员工
        dp_list = staff_db.query_staff_by_department_id(dpid)
    else:
        dp_list = staff_db.query_staff_list()
    eles = ""
    for item in dp_list:
        if item.sid == sid:
            ele = """<option value={0} selected=selected >{1}</option>""".format(item.sid, item.name)
        else:
            ele = """<option value={0} >{1}</option>""".format(item.sid, item.name)
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
    job_title_list = job_title_db.query_job_title_list()
    eles = ""
    for item in job_title_list:
        ele = """<option value={0}>{1}</option>""".format(item.id, item.job_title)
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_project():
    """创建选择项目下拉"""
    s_project_list = select_project_db.project_list()
    eles = ""
    for item in s_project_list:
        ele = """<option value={0}>{1}</option>""".format(item.id, item.name)
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_cause():
    """创建离职的原因下拉"""
    cause = reasonscause_db.reasons_cause_db()
    eles = ""
    for item in cause:
        ele = """<option value={0}>{1}</option>""".format(item.id, item.cause)
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_article():
    """创建用品"""
    article_list = assets_db.query_assets_by_list()
    eles = ""
    for item in article_list:
        ele = """<option value={0} name="article_list">{1}</option>""".format(item.nid, item.name)
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_people():
    """创建工作交接人下拉"""
    people_list = rea_people_db.people_db()
    eles = ""
    for item in people_list:
        ele = """<option value={0}>{1}</option>""".format(item.id, item.name)
        eles += ele
    return mark_safe(eles)


@register.simple_tag
def fetch_perfor_p_list(id):
    if id:
        p_list = performanceyg_db.query_perfor_by_p_id(id)
        return p_list

@register.simple_tag
def fetch_labor_c_list(id):
    if id:
        l_list = laborcontract_db.query_labor_by_c_id(id)
        return l_list

@register.simple_tag
def fetch_reasons_l_list(id):
    if id:
        l_list = reasonsleave_db.query_reasons_by_l_id(id)
        return l_list

@register.simple_tag
def fetch_social_s_list(id):
    if id:
        s_list = socialsecurity_db.query_social_by_s_id(id)
        return s_list

@register.simple_tag
def fetch_supplies_s_list(id):
    if id:
        s_list = supplies_db.query_supp_by_s_id(id)
        return s_list

@register.simple_tag
def fetch_supplies_r_list(id):
    if id:
        s_list = suppliesreturn_db.query_supp_by_s_id(id)
        return s_list


# 收支管理
@register.simple_tag
def fetch_revenue_r_list(id):
    if id:
        s_list = revenue_db.query_revenue_by_r_id(id)
        return s_list




