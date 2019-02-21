import json
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from django.contrib import auth
from django.contrib.auth import authenticate ,login
from django.views.generic.base import View

from .forms.form import LoginForm
from article.models import Posts
from django.urls import reverse


# Create your views here.

def Logout(request):
    auth.logout(request)
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
            user = auth.authenticate(username=_username, password=_password)
            if not user:
                result['message'] = '用户名或密码错误'
            else:
                auth.login(request, user)
                if hasattr(user,"staff"):
                    user_obj = user.staff
                    request.session["user_info"] = {"user_id": user_obj.sid,
                                                    "user_name": user_obj.name}
                    init_permission(user_obj, request)
                    # print("redirect")
                    # return HttpResponseRedirect('/index')
                    result['status'] = True
                    return HttpResponse(json.dumps(result))

        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            result['message'] = firsterror
        return HttpResponse(json.dumps(result))
        # return render(request, "login.html", {'msg': result['message']})
