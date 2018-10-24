import json
import uuid
import os
from django.db import transaction
from django.core import serializers
from django.shortcuts import render,HttpResponse
from task.utils import build_attachment_info
from .server import *
from .forms.form import *
from common.functions import *
from .models import *
from .templatetags.personnel_tags import *

# Create your views here.


def job_rank_list(request):
    query_sets = job_rank_db.query_job_rank_list()
    return render(request,"personnel/job_rank_list.html",{"query_sets":query_sets})


def job_rank_edit(request):
    """"职级添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            job_rank_obj = job_rank_db.query_job_rank_by_id(id)
        else:
            id = 0
            job_rank_obj = []
        return render(request, 'personnel/job_rank_edit.html', {"job_rank_obj": job_rank_obj, "id": id})
    else:
        form = JobRankForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", "")
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = job_rank_db.query_job_rank_by_id(id)
                    final_info = compare_fields(JobRank._update, record, data)
                    if final_info:
                        final_info["id"] = id
                        job_rank_db.update_job_rank(final_info)
                    ret["data"] = id
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    job_rank_db.insert_job_rank(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def job_title_list(request):
    query_sets = job_title_db.query_job_title_list()
    return render(request,"personnel/job_title_list.html",{"query_sets":query_sets})


def job_title_edit(request):
    """"职称添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            job_title_obj = job_title_db.query_job_title_by_id(id)
        else:
            id = 0
            job_title_obj = []
        return render(request, 'personnel/job_title_edit.html', {"job_title_obj": job_title_obj, "id": id})
    else:
        form = JobTitlekForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", "")
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = job_title_db.query_job_title_by_id(id)
                    final_info = compare_fields(JobTitle._update, record, data)
                    if final_info:
                        final_info["id"] = id
                        job_title_db.update_job_title(final_info)
                    ret['status'] = True
                    ret["data"] = id
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    job_title_db.insert_job_title(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def company_list(request):
    query_sets = company_db.query_company_list()
    return render(request,"personnel/company_list.html",{"query_sets":query_sets})


def company_edit(request):
    """"部门添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            company_obj = company_db.query_company_by_id(id)
        else:
            id = 0
            company_obj = []
        return render(request, 'personnel/company_edit.html', {"company_obj": company_obj, "id": id})
    else:
        form = CompanyForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", 0)
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = company_db.query_company_by_id(id)
                    final_info = compare_fields(Company._update,record,data)
                    if final_info:
                        final_info["id"] = id
                        company_db.update_company(final_info)
                    ret['status'] = True
                    ret['data'] = id
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    company_db.insert_company(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def project_list(request):
    query_sets = project_db.query_project_list()
    return render(request,"personnel/project_list.html",{"query_sets":query_sets})


def project_edit(request):
    """"部门添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            project_obj = project_db.query_project_by_id(id)
        else:
            id = 0
            project_obj = []
        return render(request, 'personnel/project_edit.html', {"project_obj": project_obj, "id": id})
    else:
        form = ProjectForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", "")
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = project_db.query_project_by_id(id)
                    final_info = compare_fields(Project._update,record, data)
                    if final_info:
                        final_info["id"] = id
                        project_db.update_project(final_info)
                    ret["data"] = id
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    project_db.insert_project(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def department_list(request):
    query_sets = department_db.query_department_list()
    return render(request,"personnel/department_list.html",{"query_sets":query_sets})


def department_edit(request):
    """"部门添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            department_obj = department_db.query_department_by_id(id)
        else:
            id = 0
            department_obj = []
        return render(request, 'personnel/department_edit.html', {"department_obj": department_obj, "id": id})
    else:
        form = DepartmentForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", "")
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = department_db.query_department_by_id(id)
                    # 对比数据是否有修改
                    final_info = compare_fields(Department._update,record,data)
                    if final_info:
                        final_info["id"] = id
                        department_db.update_deaprtment(final_info)
                    ret["data"] = id
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    department_db.insert_department(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def staff_list(request):
    query_sets = staff_db.query_staff_list()
    return render(request,"personnel/staff_list.html",{"query_sets":query_sets})


def staff_edit(request):
    mothod = request.method
    if mothod == "GET":
        sid = request.GET.get("sid","")
        if sid:
            # 更新
            query_sets = staff_db.query_staff_by_id(sid)
            life_photo = staff_life_photo_db.query_life_photo_by_sid(sid)
            staff_attach = staff_attach_db.query_staff_attachment_by_sid(sid)
            if not life_photo:
                life_photo = ""
            if not staff_attach:
                staff_attach = ""
        else:
            query_sets = {}
            life_photo = {}
            staff_attach = {}
        return render(request, "personnel/staff_edit.html", {"query_set": query_sets,
                                                             "life_photo": life_photo,
                                                             "staff_attach": staff_attach,
                                                             "sid": sid})
    else:
        ret = {'status': False, "data": '', "message": ""}
        form = StaffForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            life_photo = data.get("life_photo",None)
            staff_attach = data.get("attach",None)
            sid = data.get("sid", None)
            life_photo = json.loads(life_photo)
            staff_attach = list(json.loads(staff_attach))
            if sid:
                # 更新
                try:
                    with transaction.atomic():
                        # 更新人事信息
                        record = staff_db.query_staff_by_id(sid)
                        staff_info = compare_fields(Staff._update,record,data)
                        if staff_info:
                            staff_info["sid"] = sid
                            staff_db.update_staff(staff_info)
                        # 插入人事生活照
                        photo_record = staff_life_photo_db.query_life_photo_by_sid(sid)
                        if life_photo:
                            # 数据对比
                            if photo_record:
                                final_photo = compare_fields(StaffLifePhoto._update, photo_record, life_photo)
                                final_photo["sid_id"] = sid
                                if final_photo:
                                    staff_life_photo_db.update_photo(final_photo)
                            else:
                                staff_life_photo_db.insert_life_photo(life_photo)
                        else:
                            # 删除旧数据
                            if photo_record:
                                staff_life_photo_db.delete_photo_by_sid(sid)
                        if staff_attach:
                            # 更新附件
                            att_record = staff_attach_db.query_staff_attachment_by_sid(sid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, staff_attach, "said")
                            if insert_att:
                                insert_att = build_attachment_info({"sid_id": sid}, insert_att)
                                staff_attach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                staff_attach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                staff_attach_db.mutil_delete_task_attachment(delete_id_att)
                        ret['status'] = True
                        ret['data'] = sid
                except Exception as e:
                    print(e)
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入人事信息
                        staff_info = filter_fields(Staff._insert,data)
                        sid = staff_db.insert_staff(staff_info)
                        life_photo["sid_id"]=sid
                        # 插入人事生活照
                        if life_photo:
                            staff_life_photo_db.insert_life_photo(life_photo)
                        if staff_attach:
                            staff_attach = build_attachment_info({"sid_id":sid}, staff_attach)
                            staff_attach_db.mutil_insert_attachment(staff_attach)
                        ret['status'] = True
                        ret['data'] = sid
                except Exception as e:
                    print(e)
                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def staff_detail(request):
    id = request.GET.get("id",None)
    ret={"status":False,"data":"","message":""}
    if id:
        try:
            staff_obj = staff_db.query_staff_by_id(id)
            if staff_obj:
                # 格式化数据
                staff_json = staff_obj.__dict__
                staff_json.pop('_state')
                staff_json["gender"] = change_to_sex(staff_json["gender"])
                staff_json['company_id'] = change_to_company(staff_json['company_id'])
                staff_json['project_id'] = change_to_project(staff_json['project_id'])
                staff_json['department_id'] = change_to_department(staff_json['department_id'])
                staff_json['job_rank_id'] = change_to_job_rank(staff_json['job_rank_id'])
                staff_json['job_title_id'] = change_to_job_title(staff_json['job_title_id'])
                staff_json['is_lunar'] = change_to_lunar(staff_json['is_lunar'])
                staff_photo = staff_life_photo_db.query_life_photo_by_sid(id)
                staff_attach = staff_attach_db.query_staff_attachment_by_sid(id)
                if staff_photo:
                    staff_json['photo'] = staff_photo.life_photo
                else:
                    staff_json['photo'] = ''
                if staff_attach:
                    staff_json['attach'] = serializers.serialize("json",staff_attach)
                else:
                    staff_json['attach'] = ''
                ret['status'] = True
                ret['data'] = staff_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request,'404.html')


def staff_delete(request):
    """人事软删除"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    status = {"delete_status": 0}
    try:
        staff_db.multi_delete(id_list, status)
        ret['status'] = True
    except Exception as e:
        print(e)
        ret['status'] = "删除失败"
    return HttpResponse(json.dumps(ret))


def life_photo(request):
    """生活照片上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/personnel/life_photo"
    try:
        # 获取文件对象
        file_obj = request.FILES.get("file")
        raw_name = file_obj.name
        postfix = raw_name.split(".")[-1]
        if file_obj:
            file_name = str(uuid.uuid4())+"."+postfix
            if not os.path.exists(os.path.dirname(target_path)):
                os.makedirs(target_path)
            file_path = os.path.join(target_path, file_name)
            # os.path.join()在Linux/macOS下会以斜杠（/）分隔路径，而在Windows下则会以反斜杠（\）分隔路径,
            # 故统一路径将'\'替换成'/'
            file_path = file_path.replace('\\',"/")
            with open(file_path, "wb") as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
            ret["status"] = True
            ret["data"]['path'] = file_path
            ret["data"]['name'] = raw_name
    except Exception as e:
        ret["summary"] = str(e)
    return HttpResponse(json.dumps(ret))


def staff_attach(request):
    """生活照片上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path="media/upload/personnel/attach"
    try:
        # 获取文件对象
        file_obj = request.FILES.get("file")
        raw_name = file_obj.name
        postfix = raw_name.split(".")[-1]
        if not file_obj:
            pass
        else:
            file_name = str(uuid.uuid4()) + "." + postfix
            # 查看路径是否存在，没有则生成
            if not os.path.exists(os.path.dirname(target_path)):
                os.makedirs(target_path)
            file_path = os.path.join(target_path, file_name)
            # os.path.join()在Linux/macOS下会以斜杠（/）分隔路径，而在Windows下则会以反斜杠（\）分隔路径,
            # 故统一路径将'\'替换成'/'
            file_path = file_path.replace('\\', "/")
            with open(file_path, "wb") as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
            ret["status"] = True
            ret["data"]['path'] = file_path
            ret["data"]['name'] = raw_name
    except Exception as e:
        ret["summary"] = str(e)
    return HttpResponse(json.dumps(ret))