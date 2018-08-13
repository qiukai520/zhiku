import xadmin
from xadmin import views
from .models import *

# settings


# admin models

class DepartmentAdmin(object):
    """部门后台管理"""
    list_display = ['id',"department"]
    list_filter = ["department"]
    search_fields = ['department']
    model_icon = 'fa fa-user'


class ProjectAdmin(object):
    """项目后台管理"""
    list_display = ['id', "project"]
    list_filter = ["project"]
    search_fields = ['project']
    model_icon = 'fa fa-user'


class JobRankAdmin(object):
    """职级后台管理"""
    list_display = ['id', "rank"]
    list_filter = ["rank"]
    search_fields = ['rank']
    model_icon = 'fa fa-user'


class JobTitleAdmin(object):
    """职称后台管理"""
    list_display = ['id', "job_title"]
    list_filter = ["job_title"]
    search_fields = ['job_title']
    model_icon = 'fa fa-user'


class StaffAdmin(object):
    """员工后台管理"""
    list_display = ['sid','job_number','name',"sex","user","phone","company","department","job_rank","hire_day"]
    list_filter = ['name', "department"]
    search_fields = ['name', 'department', ]
    model_icon = 'fa fa-user'
    style_fields = {'roles': 'm2m_transfer'}


# settings


#  admin models

xadmin.site.register(Department, DepartmentAdmin)
xadmin.site.register(Project, ProjectAdmin)
xadmin.site.register(JobRank, JobRankAdmin)
xadmin.site.register(JobTitle, JobTitleAdmin)
xadmin.site.register(Staff, StaffAdmin)


