import re
from django.template import Library
from django.conf import settings
# from personnel.models import Staff2Role
register=Library()

@register.inclusion_tag("rbac/xxxxx.html")
def menu_html(request):
    """
    去Session中获取菜单相关信息，匹配当前URL，生成菜单
    :param request:
    :return:
    """
    menu_list=request.session.get(settings.PERMISSION_MENU_KEY)
    current_url=request.path_info
    # print(current_url)
    # print(menu_list)
    menu_dict={}
    for item in menu_list:
        if not item["menu_gp_id"]:
            menu_dict[item["id"]]=item
    for item in menu_list:
        regex="^{0}$".format(item["url"])
        if re.match(regex,current_url):
            menu_gp_id=item["menu_gp_id"]
            if menu_gp_id:
                menu_dict[menu_gp_id]["active"]=True
            else:
                menu_dict[item["id"]]["active"]=True
    # print(menu_dict)
    result = {}
    for item in menu_dict.values():
        active=item.get("active")
        menu_id = item["menu_id"]
        if menu_id in result:
            result[menu_id]["children"].append({"title":item["title"],"url":item["url"],"active":active})
            if active:
                result[menu_id]["active"]= True
        else:
            result[menu_id]={
                    "menu_id":item["menu_id"],
                    "menu_title":item["menu_title"],
                    "active":active,
                    "children":[{
                        "title":item["title"],
                        "url":item["url"],
                        "active":active
                    }]
                }
    # print(result)
    return {"menu_dict":result}
from rbac.models import *

@register.simple_tag
def fetch_user_role(user):
    if user:
        sid = user.staff.sid
        # roles_list = Staff2Role.objects.filter(staff_id=sid).select_related("role").all()
        roles_list=user.staff.roles.all()
        name = ''
        for item in roles_list:
            # role = Role.objects.filter(id=item.role_id).first()
            name += item.title + ";"
        return name

@register.simple_tag
def fetch_menu_key(request):
    key = settings.PERMISSION_MENU_KEY
    return key

