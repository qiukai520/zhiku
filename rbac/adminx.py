import xadmin
from xadmin import views
from .models import *

# settings


# admin models

class MenuAdmin(object):
    """菜单组"""
    # 数据展示
    list_display = ['title',]
    field = [ 'title']
    # 筛选(后台管理页面中的过滤器)
    list_filter = ['title']
    # 查询
    search_fields = ['title',]
    # 后台自定义默认排序
    # 后台直接在表上修改数据
    list_editable = []
    # 自定义后台系统的icon
    model_icon = 'fa fa-cog'
    # xadmin/plugins/refresh插件定时刷新页面
    refresh_times = [60]  # 后台可选择10秒刷新一次或者60秒刷新一次
    # 后台自定义字段只可读
    readonly_fields = []


class GroupAdmin(object):
    """菜单组"""
    # 数据展示
    list_display = ['caption',"menu" ]
    # 筛选(后台管理页面中的过滤器)
    list_filter = ['caption']
    # 查询
    search_fields = ['menu',"caption" ]
    # 后台自定义默认排序
    # 后台直接在表上修改数据
    list_editable = []
    # 自定义后台系统的icon
    model_icon = 'fa fa-cog'
    # xadmin/plugins/refresh插件定时刷新页面
    refresh_times = [60]  # 后台可选择10秒刷新一次或者60秒刷新一次
    # 后台自定义字段只可读
    readonly_fields = []


class PermissionAdmin(object):
    """权限表"""
    # 数据展示
    list_display = ['title', "url","menu_gp","code","group"]
    # 筛选(后台管理页面中的过滤器)
    list_filter = ['title',]
    # 查询
    search_fields = ['title',]
    # 后台自定义默认排序
    # 后台直接在表上修改数据
    list_editable = []
    # 自定义后台系统的icon
    model_icon = 'fa fa-cog'
    # xadmin/plugins/refresh插件定时刷新页面
    refresh_times = [60]  # 后台可选择10秒刷新一次或者60秒刷新一次
    # 后台自定义字段只可读
    readonly_fields = []


class RoleAdmin(object):
    """角色表"""
    # 数据展示
    list_display = ['title', "permission"]
    # 筛选(后台管理页面中的过滤器)
    list_filter = ['title',]
    # 查询
    search_fields = ['title',]
    # 后台自定义默认排序
    # 后台直接在表上修改数据
    list_editable = []
    # 自定义后台系统的icon
    model_icon = 'fa fa-cog'
    # xadmin/plugins/refresh插件定时刷新页面
    refresh_times = [60]  # 后台可选择10秒刷新一次或者60秒刷新一次
    # 后台自定义字段只可读
    readonly_fields = []
    style_fields = {'permission': 'm2m_transfer'}

# settings


xadmin.site.register(Menu,MenuAdmin)
xadmin.site.register(Group,GroupAdmin)
xadmin.site.register(Permission,PermissionAdmin)
xadmin.site.register(Role,RoleAdmin)



