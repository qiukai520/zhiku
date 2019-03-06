import json
import datetime
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
from django.views.generic.base import View
from .forms.form import LoginForm,PwdForm
from article.models import Posts
from rbac.models import Role,User as UserProfile,User2Role,UserLog

# login
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.middleware.csrf import rotate_token
from django.utils.crypto import constant_time_compare
from django.core.exceptions import ImproperlyConfigured, PermissionDenied

SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'
HASH_SESSION_KEY = '_auth_user_hash'
REDIRECT_FIELD_NAME = 'next'
# Create your views here.

# 重写django登录类


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 可以通过email\mobile....账号进行账号登录
            print("authenticate",username)
            user = UserProfile.objects.filter(username=username).first()
            # check_password 验证用户的密码是否正确
            print("user_obj",user)
            print("pwd",password)
            print("user_check", user.check_password(password))
            if user.check_password(password):
                return user
            else:
                return None
        except Exception as e:
            print(e)
            pass


c_auth = CustomBackend()


def get_user_model():
    """
    Return the User model that is active in this project.
    """
    try:
        return django_apps.get_model(settings.AUTH_USER_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("AUTH_USER_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL refers to model '%s' that has not been installed" % settings.AUTH_USER_MODEL
        )

def _get_user_session_key(request):
    # This value in the session is always serialized to a string, so we need
    # to convert it back to Python whenever we access it.
    return get_user_model()._meta.pk.to_python(request.session[SESSION_KEY])


# 自定义保存登录登录
def do_login(request, user, backend=None):
    """
    Persist a user id and a backend in the request. This way a user doesn't
    have to reauthenticate on every request. Note that data set during
    the anonymous session is retained when the user logs in.
    """
    print("user_login",user)
    print("dir",dir(user))
    if user is None:
        request.user = user

    if SESSION_KEY in request.session:
            request.session.flush()
    else:
        request.session.cycle_key()

    print("request.session",request.session)
    request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
    # request.session[BACKEND_SESSION_KEY] = backend
    # request.session[HASH_SESSION_KEY] = session_auth_hash
    # if hasattr(request, 'user'):
    #     request.user = user
    rotate_token(request)
    # user_logged_in.send(sender=user.__class__, request=request, user=user)


def Logout(request):
    request.session.flush()
    return redirect('/index/')


# def login(request):
#     """
#        登陆
#        :param request:
#        :return:
#        """
#     from rbac.service.init_permission import init_permission
#     next_url = request.GET.get("next", None)
#     if request.method == 'GET':
#         return render(request, 'login.html')
#     elif request.method == 'POST':
#         if not next_url:
#             next_url = "index"
#         result = {'status': False, 'message': None, 'data': None, 'next_url': next_url}
#         form = LoginForm(data=request.POST)
#         if form.is_valid():
#             _username = form.cleaned_data.get('username')
#             _password = form.cleaned_data.get('password')
#             user = auth.authenticate(username=_username, password=_password)
#             if not user:
#                 result['message'] = '用户名或密码错误'
#             else:
#                 auth.login(request, user)
#                 if hasattr(user,"staff"):
#                     user_obj = user.staff
#                     request.session["user_info"] = {"user_id": user_obj.sid,
#                                                     "user_name": user_obj.name}
#                     init_permission(user_obj, request)
#                     result['status'] = True
#         else:
#             errors = form.errors.as_data().values()
#             firsterror = str(list(errors)[0][0])
#             result['message'] = firsterror
#         return HttpResponse(json.dumps(result))


class LoginView(View):
    def get(self, request):
        # 添加一个初始用户
        # user = UserProfile.objects.get_or_create(**{"username":"lizhihong","password":"a741258963","email":'2419636244@qq.com'})
        # print("user",user)
        post = Posts.objects.all()[:6]  #取出最新的6篇文章

        return render(request, 'login.html', {"post":post})

    def post(self,request):
        from rbac.service.init_permission import init_permission
        next_url = request.GET.get("next", None)
        if not next_url:
            next_url = '/index'
        result = {'status': False, 'message': None, 'data': None, 'next_url': next_url}
        form = LoginForm(data=request.POST)
        if form.is_valid():
            _username = form.cleaned_data.get('username')
            _password = form.cleaned_data.get('password')
            user = c_auth.authenticate(request,username=_username, password=_password)
            if not user:
                result['message'] = '用户名或密码错误'
            else:
                try:
                    auth.login(request,user)

                    request.session["user_info"] = {"user_id": user.id,
                                                    "user_name": user.username}
                    init_permission(user, request)
                    result['status'] = True
                except Exception as e:
                    print(e)
                return HttpResponse(json.dumps(result))

        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            result['message'] = firsterror
        return HttpResponse(json.dumps(result))
        # return render(request, "login.html", {'msg': result['message']})


############ 用户管理 ###########

def user_center(request):
    user = User.objects.get(username=request.user)

    if request.method == 'GET':
        return render(request, 'rbac/user_center.html', locals())

    elif request.method == 'POST':
        if request.POST.get('password'):
            try:
                user.set_password(request.POST.get('password'))
                user.save()
                return JsonResponse({"code": 200, "data": None, "msg": "密码更新完毕，请重新使用新密码登录！"})
            except Exception as e:
                return JsonResponse({"code": 500, "data": None, "msg": "密码修改失败：%s" % str(e)})
        elif request.POST.get('mobile'):
            try:
                user.mobile = request.POST.get('mobile')
                user.save()
                return JsonResponse({"code": 200, "data": request.POST.get('mobile'), "msg": "手机号码更新完毕！"})
            except Exception as e:
                return JsonResponse({"code": 500, "data": None, "msg": "手机号码修改失败：%s" % str(e)})
        elif request.FILES.get('avatar'):
            try:
                avatar = request.FILES.get('avatar')
                user.image = avatar
                user.save()
                return JsonResponse({"code": 200, "data": None, "msg": "头像更新完毕！"})
            except Exception as e:
                return JsonResponse({"code": 500, "data": None, "msg": "头像更新失败：%s" % str(e)})


def get_user_list(request):
    user_list = UserProfile.objects.filter(is_staff=0).all().select_related("staff")
    groups = Role.objects.filter().all().select_related()
    # permissions = Permission.objects.all().select_related()
    return render(request, 'rbac/user_list.html', locals())



# @permission_required('users.add_userprofile', raise_exception=True)


def create_user(request):
    if request.method == 'POST':
        try:
            is_exist = UserProfile.objects.filter(username=request.POST.get('username'))
            if is_exist:
                raise Exception("用户名已存在")
            with transaction.atomic():
                user_obj = UserProfile.objects.create(
                    username=request.POST.get('username'),
                    password=make_password('123456'),
                    is_active=request.POST.get('is_active'),
                )
                data = {
                    'id': user_obj.id,
                    'username': user_obj.username,
                    'is_active': user_obj.is_active,
                }

                roles = request.POST.getlist('groups')
                if roles:
                    for i in roles:
                        role = Role.objects.get(id=i)
                        User2Role.objects.create(user=user_obj,role=role)
            return JsonResponse({"status":True,"code": 200, "data": data, "msg": "用户添加成功！初始密码是123456"})
        except Exception as e:
            print(e)
            return JsonResponse({"status":False,"code": 500, "data": None, "msg": "用户添加失败，原因：{}".format(e)})


# @permission_required('users.change_userprofile', raise_exception=True)
def reset_password(request, pk):
    if request.method == 'POST':
        try:
            UserProfile.objects.filter(id=pk).update(
                password=make_password('123456')
            )
            return JsonResponse({"code": 200, "data": None, "msg": "密码重置成功！密码为123456"})
        except Exception as e:
            print(e)
            return JsonResponse({"code": 500, "data": None, "msg": "密码重置失败，原因：{}".format(e)})


def change_password(request, pk):
    if request.method == 'POST':
        result={"code": 500,"status":False, "data": None, "msg": "密码修改成功！"}
        print("data",request.POST)
        form = PwdForm(data=request.POST)
        if form.is_valid():
            raw_pwd = form.cleaned_data.get('raw_pwd')
            new_pwd = form.cleaned_data.get('new_pwd')
            check_pwd = form.cleaned_data.get('check_pwd')
            user = UserProfile.objects.filter(id=pk).first()
            try:
                if not user.password == make_password(raw_pwd):
                    raise Exception("原始密码不正确")
                elif new_pwd != check_pwd:
                    raise Exception("两次密码输入不匹配")
                else:
                    user.password = make_password(new_pwd)
                    user.save()
                    result["code"] = 200
                    result["msg"] = "密码修改成功"
                    result["status"] = True
                return JsonResponse()
            except Exception as e:
                print(e)
                result["msg"] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            result['msg'] = firsterror
        print("result",result)
        return HttpResponse(json.dumps(result))


# @permission_required('users.add_userlog', raise_exception=True)
def get_user_log(request):
    if request.method == 'GET':
        user_logs = UserLog.objects.all()
        return render(request, 'rbac/user_log.html', locals())
    elif request.method == 'POST':
        start_time = request.POST.get('startTime')
        end_time = request.POST.get('endTime')
        new_end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d') + datetime.timedelta(1)
        end_time = new_end_time.strftime('%Y-%m-%d')
        try:
            records = []
            user_logs = UserLog.objects.filter(c_time__gt=start_time, c_time__lt=end_time)
            for user_log in user_logs:
                record = {
                    'id': user_log.id,
                    'user': user_log.user.username,
                    'remote_ip': user_log.remote_ip,
                    'content': user_log.content,
                    'c_time': user_log.c_time
                }
                records.append(record)
            return JsonResponse({'code': 200, 'records': records})
        except Exception as e:
            return JsonResponse({'code': 500, 'error': '查询失败：{}'.format(e)})
