import xadmin
from xadmin import views
from .models import *

# settings


# admin models

class CompanyAdmin(object):
    """部门后台管理"""
    list_display = ["company"]
    list_filter = ["company"]
    search_fields = ['company']
    model_icon = 'fa fa-user'


class DepartmentAdmin(object):
    """部门后台管理"""
    list_display = ["department"]
    list_filter = ["department"]
    search_fields = ['department']
    model_icon = 'fa fa-user'


class ProjectAdmin(object):
    """项目后台管理"""
    list_display = ["project"]
    list_filter = ["project"]
    search_fields = ['project']
    model_icon = 'fa fa-user'


class JobRankAdmin(object):
    """职级后台管理"""
    list_display = [ "rank"]
    list_filter = ["rank"]
    search_fields = ['rank']
    model_icon = 'fa fa-user'


class JobTitleAdmin(object):
    """职称后台管理"""
    list_display = ["job_title"]
    list_filter = ["job_title"]
    search_fields = ['job_title']
    model_icon = 'fa fa-user'


class StaffAdmin(object):
    """员工后台管理"""
    # list_display_links = ("job_number",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['job_number']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['job_number','name',"gender","user","phone","company","department","job_rank","hire_day","delete_status"]
    list_filter = ['name', "department","delete_status"]
    search_fields = ['name', 'department',]
    ordering = ['-delete_status']
    model_icon = 'fa fa-user'
    style_fields = {'roles': 'm2m_transfer'}


# settings


#  admin models
xadmin.site.register(Company, CompanyAdmin)
xadmin.site.register(Department, DepartmentAdmin)
xadmin.site.register(Project, ProjectAdmin)
xadmin.site.register(JobRank, JobRankAdmin)
xadmin.site.register(JobTitle, JobTitleAdmin)
xadmin.site.register(Staff, StaffAdmin)


