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
    """部门后台管理"""
    list_display = ['id',"project"]
    list_filter = ["project"]
    search_fields = ['project']
    model_icon = 'fa fa-user'


class JobRankAdmin(object):
    """部门后台管理"""
    list_display = ['id', "rank"]
    list_filter = ["rank"]
    search_fields = ['rank']
    model_icon = 'fa fa-user'


class StaffAdmin(object):
    """后台管理"""
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
xadmin.site.register(Staff, StaffAdmin)


