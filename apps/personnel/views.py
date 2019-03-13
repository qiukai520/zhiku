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


def select_project_list(request):
    query_sets = select_project_db.project_list()
    return render(request,"personnel/select_project_list.html",{"query_sets":query_sets})

def select_project_edit(request):
    """"选择项目添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            select_project_obj = select_project_db.query_s_title_by_id(id)
        else:
            id = 0
            select_project_obj = []
        return render(request, 'personnel/select_project_edit.html', {"select_project_obj": select_project_obj, "id": id})
    else:
        form = Select_ProjectForm(data=request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", "")
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = select_project_db.query_s_title_by_id(id)
                    final_info = compare_fields(Select_Project._update, record, data)
                    if final_info:
                        final_info["id"] = id
                        select_project_db.update_select_project_title(final_info)
                    ret['status'] = True
                    ret["data"] = id
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    select_project_db.insert_select_project_title(data)
                    ret['status'] = True
                except Exception as e:
                    ret['message'] = str(e)
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
    return HttpResponse(json.dumps(ret))


def cause_list(request):
    query_sets = reasonscause_db.reasons_cause_db()
    return render(request, "personnel/cause_list.html", {"query_sets": query_sets})

def cause_edit(request):
    """"选择项目添加或编辑"""
    method = request.method
    if method == "GET":
        id = request.GET.get("id", "")
        # 有则为编辑 ,无则添加
        if id:
            cause_obj = reasonscause_db.query_cause_by_id(id)
        else:
            id = 0
            cause_obj = []
        return render(request, 'personnel/cause_edit.html', {"cause_obj": cause_obj, "id": id})
    else:
        form = ReasonsCauseForm(data=request.POST)
        print(request.POST)
        ret = {'status': False, "data": '', "message": ""}
        if form.is_valid():
            id = request.POST.get("id", "")
            data = request.POST
            data = data.dict()
            # 有则为编辑 ,无则添加
            if id:
                try:
                    record = reasonscause_db.query_cause_by_id(id)
                    final_info = compare_fields(ReasonsCause._update, record, data)
                    if final_info:
                        final_info["id"] = id
                        reasonscause_db.update_cause_title(final_info)
                    ret['status'] = True
                    ret["data"] = id
                except Exception as e:
                    ret['message'] = str(e)
            else:
                try:
                    reasonscause_db.insert_cause_title(data)
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
    return render(request,"personnel/staffs.html",{"query_sets":query_sets})

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

def staff_edit1(request):
    mothod = request.method
    print(request.GET)
    if mothod == "GET":
        nid = request.GET.get("id", "")
        cid = request.GET.get("cid", '')
        if cid:
            customer_obj = staff_db.query_staff_by_id(cid)
            if customer_obj:
                if nid:
                    # 更新
                    query_set = performanceyg_db.query_perfor_by_id(nid)
                    edit1_attach = perforygattach_db.query_perfor_attachment(nid)
                    if not edit1_attach:
                        edit1_attach = ''
                else:
                    query_set = {}
                    edit1_attach = {}
                return render(request, "personnel/staff_edit1.html", locals())
        return render(request, "404.html")
    else:
        ret = {'status': False, "data": '', "message": ""}
        print(request.POST)
        form = PerformanceygForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            edit1_attach = data.get("attach", None)
            nid = data.get("nid", None)
            perfor_attach = list(json.loads(edit1_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        record = performanceyg_db.query_perfor_by_id(nid)
                        edit1_info = compare_fields(Performanceyg._update, record, data)
                        if edit1_info:
                            edit1_info["nid"] = nid
                            performanceyg_db.update_edit1(edit1_info)
                        # 更新附件
                        if edit1_attach:
                            att_record = perforygattach_db.query_perfor_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, perfor_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"sid_id": nid}, insert_att)
                                perforygattach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                perforygattach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                perforygattach_db.mutil_delete_task_attachment(delete_id_att)
                        else:
                            perforygattach_db.multi_delete_attach_by_edit1_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    pass
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入内容明细
                        edit1_info = filter_fields(Performanceyg._insert, data)
                        #print("edit1_info",edit1_info)

                        nid = performanceyg_db.insert_edit1(edit1_info)
                        if edit1_attach:
                            edit1_attach = build_attachment_info({"sid_id": nid}, perfor_attach)
                            perforygattach_db.mutil_insert_attachment(edit1_attach)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))



def staff_edit2(request):
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        cid = request.GET.get("cid", '')
        print(request.GET)
        if cid:
            customer_obj = staff_db.query_staff_by_id(cid)
            if customer_obj:
                if nid:
                    # 更新
                    query_set = laborcontract_db.query_labor_by_id(nid)
                    edit2_attach = laborattach_db.query_labor_attachment(nid)
                    if not edit2_attach:
                        edit2_attach = ''
                else:
                    query_set = {}
                    edit2_attach = {}
                return render(request, "personnel/staff_edit2.html", locals())
        return render(request, "404.html")
    else:
        ret = {'status': False, "data": '', "message": ""}
        print("request.POST", request.POST)
        form = LaborContractForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            edit2_attach = data.get("attach", None)
            nid = data.get("nid", None)
            labor_attach = list(json.loads(edit2_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        record = laborcontract_db.query_labor_by_id(nid)
                        edit2_info = compare_fields(Staff._update, record, data)
                        if edit2_info:
                            edit2_info["nid"] = nid
                            laborcontract_db.update_edit2(edit2_info)
                        # 更新附件
                        if edit2_attach:
                            att_record = laborattach_db.query_labor_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, labor_attach, "sid")
                            if insert_att:
                                insert_att = build_attachment_info({"sid_id": nid}, insert_att)
                                laborattach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                laborattach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                laborattach_db.mutil_delete_task_attachment(delete_id_att)
                        else:
                            laborattach_db.multi_delete_attach_by_edit2_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    pass
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入备注
                        edit2_info = filter_fields(LaborContract._insert, data)
                        nid = laborcontract_db.insert_edit2(edit2_info)
                        if edit2_attach:
                            edit2_attach = build_attachment_info({"sid_id": nid}, labor_attach)
                            laborattach_db.mutil_insert_attachment(edit2_attach)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def staff_edit3(request):
    mothod = request.method
    print('mothod',mothod)
    if mothod == "GET":
        nid = request.GET.get("id", "")
        cid = request.GET.get("cid", '')
        print(request.GET)
        if cid:
            customer_obj = staff_db.query_staff_by_id(cid)
            if customer_obj:
                if nid:
                    # 更新
                    query_set = reasonsleave_db.query_reasons_by_id(nid)
                    edit3_attach = reasonsattach_db.query_reasons_attachment(nid)
                    if not edit3_attach:
                        edit3_attach = ''
                else:
                    query_set = {}
                    edit3_attach = {}
                return render(request, "personnel/staff_edit3.html", locals())
        return render(request, "404.html")
    else:
        ret = {'status': False, "data": '', "message": ""}
        print("request.POST", request.POST)
        form = ReasonsLeaveForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            edit3_attach = data.get("attach", None)
            nid = data.get("nid", None)
            reasons_attach = list(json.loads(edit3_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        record = reasonsleave_db.query_reasons_by_id(nid)
                        edit3_info = compare_fields(Staff._update, record, data)
                        if edit3_info:
                            edit3_info["nid"] = nid
                            reasonsleave_db.update_edit3(edit3_info)
                        # 更新附件
                        if edit3_attach:
                            att_record = reasonsattach_db.query_reasons_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, reasons_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"sid_id": nid}, insert_att)
                                reasonsattach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                reasonsattach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                reasonsattach_db.mutil_delete_task_attachment(delete_id_att)
                        else:
                            reasonsattach_db.multi_delete_attach_by_edit3_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    pass
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入备注
                        edit3_info = filter_fields(ReasonsLeave._insert, data)
                        nid = reasonsleave_db.insert_edit3(edit3_info)
                        if edit3_attach:
                            edit3_attach = build_attachment_info({"sid_id": nid}, reasons_attach)
                            reasonsattach_db.mutil_insert_attachment(edit3_attach)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))

def staff_edit4(request):
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        cid = request.GET.get("cid", '')
        if cid:
            customer_obj = staff_db.query_staff_by_id(cid)
            if customer_obj:
                if nid:
                    # 更新
                    query_set = socialsecurity_db.query_social_by_id(nid)
                    edit4_attach = socialattach_db.query_social_attachment(nid)
                    if not edit4_attach:
                        edit4_attach = ''
                else:
                    query_set = {}
                    edit4_attach = {}
                return render(request, "personnel/staff_edit4.html", locals())
        return render(request, "404.html")
    else:
        ret = {'status': False, "data": '', "message": ""}
        print("request.POST", request.POST)
        form = SocialSecurityForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            edit4_attach = data.get("attach", None)
            nid = data.get("nid", None)
            social_attach = list(json.loads(edit4_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        record = socialsecurity_db.query_social_by_id(nid)
                        edit4_info = compare_fields(Staff._update, record, data)
                        if edit4_info:
                            edit4_info["nid"] = nid
                            socialsecurity_db.update_edit4(edit4_info)
                        # 更新附件
                        if edit4_attach:
                            att_record = socialattach_db.query_reasons_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, social_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"sid_id": nid}, insert_att)
                                socialattach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                socialattach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                socialattach_db.mutil_delete_task_attachment(delete_id_att)
                        else:
                            socialattach_db.multi_delete_attach_by_edit4_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    pass
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入备注
                        edit4_info = filter_fields(SocialSecurity._insert, data)
                        nid = socialsecurity_db.insert_edit4(edit4_info)
                        if edit4_attach:
                            edit4_attach = build_attachment_info({"sid_id": nid}, social_attach)
                            socialattach_db.mutil_insert_attachment(edit4_attach)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))

def staff_edit5(request):
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        cid = request.GET.get("cid", '')
        if cid:
            customer_obj = staff_db.query_staff_by_id(cid)
            if customer_obj:
                if nid:
                    # 更新
                    query_set = supplies_db.query_supp_by_id(nid)
                    edit5_attach = suppliesattach_db.query_supp_attachment(nid)
                    if not edit5_attach:
                        edit5_attach = ''
                else:
                    query_set = {}
                    edit5_attach = {}
                return render(request, "personnel/staff_edit5.html", locals())
        return render(request, "404.html")
    else:
        ret = {'status': False, "data": '', "message": ""}
        print("request.POST", request.POST)
        form = SuppliesForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            edit5_attach = data.get("attach", None)
            nid = data.get("nid", None)
            supp_attach = list(json.loads(edit5_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        record = supplies_db.query_supp_by_id(nid)
                        edit5_info = compare_fields(Staff._update, record, data)
                        if edit5_info:
                            edit5_info["nid"] = nid
                            supplies_db.update_edit5(edit5_info)
                        # 更新附件
                        if edit5_attach:
                            att_record = suppliesattach_db.query_supp_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, supp_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"sid_id": nid}, insert_att)
                                suppliesattach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                suppliesattach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                suppliesattach_db.mutil_delete_task_attachment(delete_id_att)
                        else:
                            suppliesattach_db.multi_delete_attach_by_edit5_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    pass
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入备注
                        edit5_info = filter_fields(Supplies._insert, data)
                        nid = supplies_db.insert_edit5(edit5_info)
                        if edit5_attach:
                            edit5_attach = build_attachment_info({"sid_id": nid}, supp_attach)
                            suppliesattach_db.mutil_insert_attachment(edit5_attach)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))

def staff_edit6(request):
    mothod = request.method
    if mothod == "GET":
        nid = request.GET.get("id", "")
        cid = request.GET.get("cid", '')
        if cid:
            customer_obj = staff_db.query_staff_by_id(cid)
            if customer_obj:
                if nid:
                    # 更新
                    query_set = suppliesreturn_db.query_supp_by_id(nid)
                    edit6_attach = suppliesreturnattach_db.query_supp_attachment(nid)
                    if not edit6_attach:
                        edit6_attach = ''
                else:
                    query_set = {}
                    edit6_attach = {}
                return render(request, "personnel/staff_edit6.html", locals())
        return render(request, "404.html")
    else:
        ret = {'status': False, "data": '', "message": ""}
        print("request.POST", request.POST)
        form = SuppliesReturnForm(data=request.POST)
        if form.is_valid():
            data = request.POST
            data = data.dict()
            edit6_attach = data.get("attach", None)
            nid = data.get("nid", None)
            supp_attach = list(json.loads(edit6_attach))
            if nid:
                # 更新
                try:
                    with transaction.atomic():
                        record = suppliesreturn_db.query_supp_by_id(nid)
                        edit6_info = compare_fields(Staff._update, record, data)
                        if edit6_info:
                            edit6_info["nid"] = nid
                            suppliesreturn_db.update_edit5(edit6_info)
                        # 更新附件
                        if edit6_attach:
                            att_record = suppliesreturnattach_db.query_supp_attachment(nid)
                            # 数据对比
                            insert_att, update_att, delete_id_att = compare_json(att_record, supp_attach, "nid")
                            if insert_att:
                                insert_att = build_attachment_info({"sid_id": nid}, insert_att)
                                suppliesreturnattach_db.mutil_insert_attachment(insert_att)
                            if update_att:
                                suppliesreturnattach_db.mutil_update_attachment(update_att)
                            if delete_id_att:
                                suppliesreturnattach_db.mutil_delete_task_attachment(delete_id_att)
                        else:
                            suppliesreturnattach_db.multi_delete_attach_by_edit5_id(nid)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    pass
                    ret["message"] = "更新失败"
            else:
                # 创建
                try:
                    with transaction.atomic():
                        # 插入备注
                        edit6_info = filter_fields(Supplies_Return._insert, data)
                        nid = suppliesreturn_db.insert_edit6(edit6_info)
                        if edit6_attach:
                            edit6_attach = build_attachment_info({"sid_id": nid}, supp_attach)
                            suppliesreturnattach_db.mutil_insert_attachment(edit6_attach)
                        ret['status'] = True
                        ret['data'] = nid
                except Exception as e:
                    print(e)
                    ret["message"] = "添加失败"
        else:
            errors = form.errors.as_data().values()
            firsterror = str(list(errors)[0][0])
            ret['message'] = firsterror
        return HttpResponse(json.dumps(ret))


def staff_detail_1(request):
    id = request.GET.get("id", None)
    ret = {"status": False, "data": "", "message": ""}
    print('ret',ret)
    if id:
        try:
            perfor_obj =performanceyg_db.query_perfor_by_id(id)
            if perfor_obj:
                # 格式化数据
                perfor_json = perfor_obj.__dict__
                perfor_json.pop('_state')
                perfor_json["select_project_id_id"] = change_to_s_project(perfor_json["select_project_id_id"])
                perfor_attach = perforygattach_db.query_perfor_attachment_by_sid(id)
                if staff_attach:
                    perfor_json['attach'] = serializers.serialize("json", perfor_attach)
                else:
                    perfor_json['attach'] = ''
                ret['status'] = True
                ret['data'] = perfor_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request,'404.html')

# def staff_detail_2(request):
#     id = request.GET.get("id", None)
#     ret = {"status": False, "data": "", "message": ""}
#     if id:
#         try:
#             staff_obj = staff_db.query_staff_by_id(id)
#             if staff_obj:
#                 #格式化数据
#                 staff_json = staff_obj.__dict__
#                 staff_json.pop('_state')
#                 staff_json["company_id"] = change_to_company(staff_json["company_id"])
#                 staff_attach = staff_attach_db.query_staff_attachment_by_sid(id)
#                 if staff_attach:
#                     staff_json['attach'] = serializers.serialize("json", staff_attach)
#                 else:
#                     staff_json['attach'] = ''
#                 ret['status'] = True
#                 ret['data'] = staff_json
#                 return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
#         except Exception as e:
#                 print(e)
#     return render(request, '404.html')

def staff_detail_2(request):
    id = request.GET.get("id", None)
    ret = {"status": False, "data": "", "message": ""}
    if id:
        try:
            labor_obj = laborcontract_db.query_labor_by_id(id)
            if labor_obj:
                # 格式化数据
                labor_json = labor_obj.__dict__
                labor_json.pop('_state')
                # labor_json["sid_id"] = change_to_company(labor_json["sid_id"])
                labor_attach = laborattach_db.query_labor_attachment(id)
                if labor_attach:
                    labor_json['attach'] = serializers.serialize("json", labor_attach)
                else:
                    labor_json['attach'] = ''
                ret['status'] = True
                ret['data'] = labor_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request, '404.html')

def staff_detail_3(request):
    id = request.GET.get("id", None)
    ret = {"status": False, "data": "", "message": ""}
    if id:
        try:
            reasons_obj = reasonsleave_db.query_reasons_by_id(id)
            if reasons_obj:
                # 格式化数据
                reasons_json = reasons_obj.__dict__
                reasons_json.pop('_state')

                reasons_json["reasons_people_id"] = change_to_p_people(reasons_json["reasons_people_id"])
                reasons_attach = reasonsattach_db.query_reasons_attachment(id)
                if reasons_attach:
                    reasons_json['attach'] = serializers.serialize("json", reasons_attach)
                else:
                    reasons_json['attach'] = ''
                ret['status'] = True
                ret['data'] = reasons_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request, '404.html')

def staff_detail_4(request):
    id = request.GET.get("id", None)
    ret = {"status": False, "data": "", "message": ""}
    if id:
        try:
            social_obj = socialsecurity_db.query_social_by_id(id)
            if social_obj:
                # 格式化数据
                social_json = social_obj.__dict__
                social_json.pop('_state')
                reasons_attach = socialattach_db.query_social_attachment(id)
                if reasons_attach:
                    social_json['attach'] = serializers.serialize("json", reasons_attach)
                else:
                    social_json['attach'] = ''
                ret['status'] = True
                ret['data'] = social_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request, '404.html')

def staff_detail_5(request):
    id = request.GET.get("id", None)
    ret = {"status": False, "data": "", "message": ""}
    if id:
        try:
            supp_obj = supplies_db.query_supp_by_id(id)
            if supp_obj:
                # 格式化数据
                supp_json = supp_obj.__dict__
                supp_json.pop('_state')
                supp_attach = suppliesattach_db.query_supp_attachment(id)
                supp_json["supplies_id_id"] = change_to_a_article(supp_json["supplies_id_id"])
                if supp_attach:
                    supp_json['attach'] = serializers.serialize("json", supp_attach)
                else:
                    supp_json['attach'] = ''
                ret['status'] = True
                ret['data'] = supp_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request, '404.html')

def staff_detail_6(request):
    id = request.GET.get("id", None)
    ret = {"status": False, "data": "", "message": ""}
    if id:
        try:
            supp_obj = suppliesreturn_db.query_supp_by_id(id)
            if supp_obj:
                # 格式化数据
                supp_json = supp_obj.__dict__
                supp_json.pop('_state')
                supp_attach = suppliesreturnattach_db.query_supp_attachment(id)
                supp_json["supplies_id_id"] = change_to_a_article(supp_json["supplies_id_id"])
                if supp_attach:
                    supp_json['attach'] = serializers.serialize("json", supp_attach)
                else:
                    supp_json['attach'] = ''
                ret['status'] = True
                ret['data'] = supp_json
                return HttpResponse(json.dumps(ret, cls=CJSONEncoder))
        except Exception as e:
            print(e)
    return render(request, '404.html')

def staff_detail(request):
    cid = request.GET.get("sid", None)
    if cid:
        query_sets = staff_db.query_staff_by_id(cid)
        if query_sets:
            life_photo = staff_life_photo_db.query_life_photo_by_sid(cid)
            # customer_licence = customer_licence_db.query_customer_licence(cid)
            life_attach = staff_attach_db.query_staff_attachment_by_sid(cid)
            if not life_photo:
                customer_photo = ''
            # if not customer_licence:
            #     customer_licence = ''
            if not life_attach:
                customer_attach = ''
            return render(request, "personnel/staff_detail.html", {"query_set": query_sets,
                                                                "life_photo": life_photo,
                                                                # "customer_licence": customer_licence,
                                                                "life_attach": life_attach,
                                                                })
    return render(request, '404.html')

def staff_delete1(request):
    """删除就职表现信息"""
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        performanceyg_db.multi_delete(id_list)
        ret['status'] = True
    except Exception as e:
        ret['message'] = "删除失败"
        print(e)
    return HttpResponse(json.dumps(ret))


def staff_delete2(request):
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        laborcontract_db.multi_delete(id_list)
        ret['status'] = True
    except Exception as e:
        ret['message'] = "删除失败"
        print(e)
    return HttpResponse(json.dumps(ret))


def staff_delete3(request):
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        reasonsleave_db.multi_delete(id_list)
        ret['status'] = True
    except Exception as e:
        ret['message'] = "删除失败"
        print(e)
    return HttpResponse(json.dumps(ret))


def staff_delete4(request):
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        socialsecurity_db.multi_delete(id_list)
        ret['status'] = True
    except Exception as e:
        ret['message'] = "删除失败"
        print(e)
    return HttpResponse(json.dumps(ret))

def staff_delete5(request):
    ret = {'status': False, "data": "", "message": ""}
    ids = request.GET.get("ids", '')
    ids = ids.split("|")
    # 转化成数字
    id_list = []
    for item in ids:
        if item:
            id_list.append(int(item))
    try:
        supplies_db.multi_delete(id_list)
        ret['status'] = True
    except Exception as e:
        ret['message'] = "删除失败"
        print(e)
    return HttpResponse(json.dumps(ret))



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


def staff_select(request):
    """获取人事数据"""
    staffs = staff_db.query_staff_list()
    staff_list = []
    for item in staffs:
        staff = dict()
        staff["roleId"] = item.sid
        staff["roleName"] = item.name
        staff_list.append(staff)
    return HttpResponse(json.dumps(staff_list))


def life_photo(request):
    """生活照片上传"""
    ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
    # 保存路径
    target_path = "media/upload/personnel/life_photo"
    if not os.path.exists(target_path):
        os.makedirs(target_path)
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
    if not os.path.exists(target_path):
        os.makedirs(target_path)
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