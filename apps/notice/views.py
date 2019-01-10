from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from . import models
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json
from .models import Notice


# Create your views here.

# @login_required
def notice_read(request, notice_id):
    user = request.user

    notice = get_object_or_404(models.Notice,user=user.staff, nid=notice_id)
    notice.notice_status = True
    notice.save()
    return HttpResponseRedirect(notice.notice_url)


# @login_required
def notice_count(request):
    user = request.user
    notice_count = user.notice_for_user.filter(notice_status=False).count()
    return JsonResponse({'notice_count': notice_count})


# @login_required
# @csrf_protect
def notice_readall(request):
    user = request.user
    error = '操作成功'
    action = request.POST.get('action')
    print("action")
    if action == 'readall':
        notice_list = user.staff.notice_for_user.filter(notice_status=False)
        for notice_get in notice_list:
            notice_get.notice_status = True
            notice_get.save()
    else:
        error = '参数错误'
    return JsonResponse({'error': error})


# @login_required
# @csrf_protect
def notice_action(request):
    user = request.user
    error = '操作成功'
    notice_id_list = request.POST.get('notice_id_list')
    notice_id_list = json.loads(notice_id_list)
    action = request.POST.get('action')
    # notice_id_list = ast.literal_eval(notice_id_list)
    for notice_id in notice_id_list:
        notice_get = get_object_or_404(models.Notice, user=user.staff, nid=notice_id)
        if action == 'delete':
            notice_get.delete()
        elif action == 'read':
            notice_get.notice_status = True
            notice_get.save()
        elif action == 'unread':
            notice_get.notice_status = False
            notice_get.save()
        else:
            error = '参数错误'
    return JsonResponse({'error': error})


# @login_required
# @csrf_protect
def notice_table_list(request):
    user = request.user
    resultdict = {}

    # page = request.POST.get('page')
    # rows = request.POST.get('limit')
    notice_type = request.POST.get('notice_type')
    if not notice_type:
        notice_type = ''
    notice_status = request.POST.get('notice_status')
    if not notice_status:
        notice_status = ['True', 'False']
    else:
        notice_status = [notice_status]
    notice_list = models.Notice.objects.filter(user=user.staff, notice_status__in=notice_status,
                                               notice_type__icontains=notice_type).order_by('-notice_time')
    total = notice_list.count()
    # notice_list = paging(notice_list, rows, page)
    data = []
    for notice in notice_list:
        dic = {}
        dic['id'] = notice.nid
        dic['notice_title'] = notice.notice_title
        dic['notice_body'] = notice.notice_body
        if notice.notice_status:
            dic['notice_status'] = '已读'
        else:
            dic['notice_status'] = '未读'
        dic['notice_time'] = notice.notice_time.strftime("%Y-%m-%d %H:%M:%S")

        data.append(dic)
    resultdict['code'] = 0
    resultdict['msg'] = "用户申请列表"
    resultdict['count'] = total
    resultdict['data'] = data
    return JsonResponse(resultdict)


# @login_required
def notice_view(request):
    return render(request, 'notice/noticelist.html')


def notice_add(user, data):
    '''           
                这里的 data 为数据字典，内容包括
    {
        'notice_title':'***',
        'notice_body':'***',
        'notice_url':'***',
        'notice_type':'***'
    }
    '''
    # user_instance=Staff.filter(sid_id=user).first()
    data["user_id"] = user
    res = Notice.objects.get_or_create(**data)
    if res[1]:
        return False
    else:
        res[0].notice_status = False
        res[0].save()
        return True