import xadmin
from xadmin import views
from .models import *

# settings


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "企业驱动·智库"      #设置头标题
    site_footer = " 企业驱动 • 智库－企业健康诊断与修复开创者"      #设置脚标题
    menu_style = "accordion"



# admin models


class TaskAdmin(object):
    """工作任务后台管理"""
    # 数据展示
    list_display = ['tid','title', 'content', 'type','cycle','create_time',]
    field = ['tid','title', 'content', 'type','cycle','create_time']
    # 筛选(后台管理页面中的过滤器)
    list_filter = ['type']
    # 查询
    search_fields =['title', 'content']
    # 后台自定义默认排序
    ordering = ['-create_time']
    # 后台直接在表上修改数据
    list_editable = []
    # 自定义后台系统的icon
    model_icon = 'fa fa-cog'
    # xadmin/plugins/refresh插件定时刷新页面
    refresh_times = [60]  # 后台可选择10秒刷新一次或者60秒刷新一次
    # 后台自定义字段只可读
    readonly_fields = []


class TaskAdmin(object):
    """工作任务后台管理"""
    # 数据展示
    show_detail_fields = ['title']  # 在指定的字段后添加一个显示数据详情的一个按钮
    list_display = ['title', 'content', 'type','cycle','create_time',]
    field = ['title', 'content', 'type','cycle','create_time']
    # 筛选(后台管理页面中的过滤器)
    list_filter = ['type']
    # 查询
    search_fields =['title', 'content']
    # 后台自定义默认排序
    ordering = ['-create_time']
    # 后台直接在表上修改数据
    list_editable = []
    # 自定义后台系统的icon
    model_icon = 'fa fa-cog'
    # xadmin/plugins/refresh插件定时刷新页面
    refresh_times = [60]  # 后台可选择10秒刷新一次或者60秒刷新一次
    # 后台自定义字段只可读
    readonly_fields = []


class TaskMapAdmin(object):
    """工作任务后台管理"""
    # 数据展示
    show_detail_fields = ['tid']  # 在指定的字段后添加一个显示数据详情的一个按钮
    list_display = ['tid','assigner', 'team', 'is_finish',"status",'cycle','start_time',"deadline",'create_time']
    # 筛选(后台管理页面中的过滤器)
    list_filter = ['team','tid']
    # 查询
    search_fields =['tid', 'content']
    # 后台自定义默认排序
    ordering = ['-create_time']
    # 后台直接在表上修改数据
    list_editable = []
    # 自定义后台系统的icon
    model_icon = 'fa fa-cog'
    # xadmin/plugins/refresh插件定时刷新页面
    refresh_times = [60]  # 后台可选择10秒刷新一次或者60秒刷新一次
    # 后台自定义字段只可读
    readonly_fields = []


class TaskAttachmentAdmin(object):
    """任务附件后台管理"""
    list_display = ['tamid','tid', 'attachment', 'name', 'description']
    list_filter = ["name"]
    search_fields = ['name']
    model_icon = 'fa fa-cog'


class TaskTagAdmin(object):
    """任务标签后台管理"""
    list_display = ['ttid', 'tid','name']
    list_filter = ["name"]
    search_fields = ['name']
    model_icon = 'fa fa-cog'


class TaskCycleAdmin(object):
    """任务周期后台管理"""
    list_display = ['tcid', "name"]
    list_filter = ["name"]
    search_fields = ['name']
    model_icon = 'fa fa-cog'


class TaskTypeAdmin(object):
    """任务类型后台管理"""
    list_display = ["tpid", 'name', ]
    list_filter = ["name"]
    search_fields = ['name']
    model_icon = 'fa fa-cog'


class TaskAssignAdmin(object):
    """任务指派后台管理"""
    show_detail_fields = ['tmid']  # 在指定的字段后添加一个显示数据详情的一个按钮
    list_display = ['tmid', 'title', 'content', 'member_id','progress', 'deadline','create_time','last_edit']
    list_filter = ['tmid','member_id', 'deadline']
    search_fields = ['title', 'content']
    fields = ['tmid', 'title', 'content', 'member_id', 'deadline','create_time','last_edit']
    model_icon = 'fa fa-cog'


class TaskAssignTagAdmin(object):
    """任务指派标签后台管理"""
    list_display = ['tat','tid', 'name' ]
    list_filter = ["name"]
    search_fields = ['name']
    model_icon = 'fa fa-cog'


class TaskAssignAttachAdmin(object):
    """任务指派附件后台管理"""
    list_display = ['taaid','tasid', 'attach', 'name', 'description']
    list_filter = ["name"]
    search_fields = ['name']
    model_icon = 'fa fa-cog'


class TaskAssignTagAdmin(object):
    """任务指派附件后台管理"""
    list_display = ['tatid','tasid', 'name' ]
    list_filter = ["name"]
    search_fields = ['name']
    model_icon = 'fa fa-cog'


class TaskReviewAdmin(object):
    """任务审核记录后台管理"""
    list_display = ["tvid",'tmid','sid','follow']
    list_filter = ['tmid']
    search_fields = []
    model_icon = 'fa fa-cog'


class TaskSubmitRecordAdmin(object):
    """任务提交记录后台管理"""
    show_detail_fields = ['tasid']  # 在指定的字段后添加一个显示数据详情的一个按钮
    list_display = ['tasid', 'title', 'summary', 'remark','completion','is_assist','create_time','last_edit']
    list_filter = []
    search_fields = ['tasid',"title"]
    model_icon = 'fa fa-cog'


class TaskSubmitTagAdmin(object):
    """任务提交标签后台管理"""
    list_display = ["tstid", 'tsid', 'name', ]
    list_filter = ["name"]
    search_fields = ['name']
    model_icon = 'fa fa-cog'


class TaskSubmitAttachmentAdmin(object):
    """任务提交附件后台管理"""
    list_display = ["tsaid",'tsid', 'attach', 'name', 'description']
    list_filter = ["name"]
    search_fields = ['name']
    model_icon = 'fa fa-cog'


class TaskReviewRecordAdmin(object):
    """任务审核记录后台管理"""
    show_detail_fields = ['tasid']  # 在指定的字段后添加一个显示数据详情的一个按钮
    list_display = ['tasid', "tvid",'is_complete', 'reason','comment', 'evaluate','create_time']
    list_filter = ['tasid']
    search_fields = []
    model_icon = 'fa fa-cog'


class PerformanceAdmin(object):
    """绩效后台管理"""
    show_detail_fields = ['name']  # 在指定的字段后添加一个显示数据详情的一个按钮
    list_display = [ "name", 'personal_score','personal_total','team_score', 'team_total']
    list_filter = ["name"]
    search_fields = ['name']
    model_icon = 'fa fa-cog'


class PerformanceRecordAdmin(object):
    """绩效后台管理"""
    list_display = ['prid','sid',"tmid", 'personal_score',"team_score"]
    list_filter = ["sid"]
    search_fields = ['sid']
    model_icon = 'fa fa-cog'




# settings
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

#  admin models
xadmin.site.register(Task, TaskAdmin)
xadmin.site.register(TaskTag, TaskTagAdmin)
xadmin.site.register(TaskAttachment, TaskAttachmentAdmin)
xadmin.site.register(TaskCycle, TaskCycleAdmin)
xadmin.site.register(TaskType,TaskTypeAdmin)
xadmin.site.register(TaskMap, TaskMapAdmin)
xadmin.site.register(TaskAssign, TaskAssignAdmin)
xadmin.site.register(TaskAssignAttach, TaskAssignAttachAdmin)
xadmin.site.register(TaskAssignTag, TaskAssignTagAdmin)
xadmin.site.register(TaskSubmitRecord, TaskSubmitRecordAdmin)
xadmin.site.register(TaskSubmitTag, TaskSubmitTagAdmin)
xadmin.site.register(TaskSubmitAttachment,TaskSubmitAttachmentAdmin)
xadmin.site.register(TaskReview, TaskReviewAdmin)
xadmin.site.register(TaskReviewRecord,TaskReviewRecordAdmin)
xadmin.site.register(Performance,PerformanceAdmin)
xadmin.site.register(PerformanceRecord,PerformanceRecordAdmin)


