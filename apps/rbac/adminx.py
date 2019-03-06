
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,)
from django.forms import ModelMultipleChoiceField
from xadmin.layout import Fieldset, Main, Side, Row, FormHelper

from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from .models import User

# User = get_user_model()
import xadmin
from xadmin import views
from .models import *

# settings


# admin models
# 重载 xadmin User
ACTION_NAME = {
    'add': _('Can add %s'),
    'change': _('Can change %s'),
    'edit': _('Can edit %s'),
    'delete': _('Can delete %s'),
    'view': _('Can view %s'),
}


def get_permission_name(p):
    action = p.codename.split('_')[0]
    if action in ACTION_NAME:
        return ACTION_NAME[action] % str(p.content_type)
    else:
        return p.name


class PermissionModelMultipleChoiceField(ModelMultipleChoiceField):

    def label_from_instance(self, p):
        return get_permission_name(p)


class UserAdmin(object):
    change_user_password_template = None
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', "roles")
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    style_fields = {'user_permissions': 'm2m_transfer',"roles": 'm2m_transfer'}
    model_icon = 'fa fa-user'
    relfield_style = 'fk-ajax'

    def get_field_attrs(self, db_field, **kwargs):
        attrs = super(UserAdmin, self).get_field_attrs(db_field, **kwargs)
        if db_field.name == 'user_permissions':
            attrs['form_class'] = PermissionModelMultipleChoiceField
        return attrs

    def get_model_form(self, **kwargs):
        if self.org_obj is None:
            self.form = UserCreationForm
        else:
            self.form = UserChangeForm
        return super(UserAdmin, self).get_model_form(**kwargs)

    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Personal info'),
                             Row('first_name', 'last_name'),
                             'email'
                             ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),
                             'last_login', 'date_joined'
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserAdmin, self).get_form_layout()


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
    model_icon =' fa-fw fa fa-group'


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
xadmin.site.register(User,UserAdmin)




