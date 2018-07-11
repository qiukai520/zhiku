import time
from datetime import datetime
from datetime import timedelta
from django import template
from django.utils.safestring import mark_safe
from task.server import *

register = template.Library()

@register.simple_tag
def build_department_ele():
    """构建部门下拉框"""
    dp_list = department_db.query_department_list()
    eles = "<option value=0 >------</option>"
    for item in dp_list:
        ele = """<option value={0} >{1}</option>""".format(item.id, item.department)
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_performence_ele():
    """构建绩效分类下拉框"""
    perfor_list = performence_db.query_performence_list()
    eles = ""
    for item in perfor_list:
        ele = """<option value={0}>{1}</option>""".format(item.pid, item.name)
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_task_execute_way_ele():
    """构建任务执行方式下拉框"""
    way_list = task_db.execute_way
    eles = ""
    for item in way_list:
      ele = """<option value={0}>{1}</option>""".format(item["execute_way"], item["caption"])
      eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_task_cycle_ele():
    """构建任务周期下拉框"""
    cycle_list = task_cycle_db.query_task_cycle_list()
    eles = ""
    for item in cycle_list:
        ele = """<option value={0}>{1}</option>""".format(item.tcid, item.name)
        eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_auditor_ele():
    """构建负责人选择框"""
    auditor_list = staff_db.query_staff_list()
    eles = "<option value=0>---</option>"
    for item in auditor_list:
        ele = """<option value={0}>{1}</option>""".format(item.sid, item.name)
        eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_task_type_filter(selected):
    """构建任务类型选择框"""
    selected=int(selected)
    task_type_list = task_type_db.query_task_type_list()
    eles = ""
    for item in task_type_list:
        if selected == item.tpid:
            ele = """<option selected=selected value={0}>{1}</option>""".format(item.tpid, item.name)
        else:
            ele = """<option value={0}>{1}</option>""".format(item.tpid, item.name)
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_task_tags_ele(tid):
    """构建任务标签"""
    ele_list = ''
    record_tags = task_tag_db.query_task_tag_by_tid(tid)
    for item in record_tags:
        if item.name:
            ele = "<span>{0};</span>".format(item.name)
            ele_list += ele
    return mark_safe(ele_list)

@register.simple_tag
def build_task_review_ele(tid):
    """构建任务标签"""
    ele_list = ''
    task_review_ids = task_review_db.query_task_reviewer_by_tid(tid).order_by("follow")
    for item in task_review_ids:
        staff = staff_db.query_staff_by_id(item.sid)
        if staff.name:
            ele = "<span>{0};</span>".format(staff.name)
            ele_list += ele
    return mark_safe(ele_list)


@register.simple_tag
def build_task_type_ele():
    """构建任务类型选择框"""
    task_type_list = task_type_db.query_task_type_list()
    eles = ""
    for item in task_type_list:
        ele = """<option value={0}>{1}</option>""".format(item.tpid, item.name)
        eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_reviewer_ele(dpid):
    """构建审核人下拉框"""
    reviewer_list = staff_db.query_staff_list()
    eles = ''
    for item in reviewer_list:
        ele = """<option value={0} ondblclick=ElementMoveTo(this,'id_staff_from','id_staff_to')>{1}</option>""".format(item.sid, item.name)
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def change_to_task_execute_way(way_id):
    way_list = task_db.execute_way
    for item in way_list:
        if int(item["execute_way"]) == way_id:
            return item["caption"]

@register.simple_tag
def change_to_task_type(tpid):
    """转化成任务类型"""
    print("tpid",tpid)
    task_type = task_type_db.query_task_type_by_id(tpid)
    return task_type.name

@register.simple_tag
def change_to_staff(id):
    """获取根据id员工"""
    issuer = staff_db.query_staff_by_id(id)
    return issuer.name

@register.simple_tag
def change_to_task_cycle(tcid):
    """获取任务周期"""
    task_cycle = task_cycle_db.query_task_cycled_by_tcid(tcid)
    return task_cycle.name

@register.simple_tag
def change_to_task_assign_status(id):
    """获取任务指派状态"""
    assign_list = task_db.is_assign
    for item in assign_list:
        if int(item["iaid"]) == id:
            return item["caption"]

@register.simple_tag
def change_to_task_status(id):
    """获取任务状态"""
    status_list = task_db.task_status
    for item in status_list:
        if int(item["id"]) == id:
            return item['caption']

@register.simple_tag
def change_to_task_perfomance(pid):
    """获取任务绩效"""
    performance = performence_db.query_performence_by_pid(pid)
    return performance.name


@register.simple_tag
def change_to_task_finish_status(id):
    """获取任务完成状态"""
    finish_list = task_db.is_finish
    for item in finish_list:
        if int(item['id']) == id:
            return item['caption']


@register.simple_tag
def change_to_task_reviewer(tvid):
    """根据tvid获取审核人"""
    task_review_obj = task_review_db.query_task_reviewer_by_tvid(tvid)
    staff_obj = staff_db.query_staff_by_id(task_review_obj.sid_id)
    return staff_obj.name

@register.simple_tag
def bulid_assign_member_list(tid):
    """构建指派对象"""
    task_assign_list = task_assign_db.query_task_assign_by_tid(tid)
    eles = """<ul>"""
    for item in task_assign_list:
        # 获取对象信息
        member = staff_db.query_staff_by_id(item.member_id_id)
        # 获取任务提交记录
        last_commit_record = task_submit_record_db.query_last_submit_record(item.tasid)
        if last_commit_record:
            completion = last_commit_record.completion
            last_edit = last_commit_record.last_edit.strftime("%Y-%m-%d")
            if completion:
                status = str(completion)+"%"
        else:
            status = "进行中"
            last_edit = ''
        # 构建指派对象列表
        ele = """<li data-toggle="modal" onclick="MemberAssignShow(this)"><span class="member_name"  >{0}</span>  &nbsp
        <span style="color: blue" class="glyphicon glyphicon-plus plus " ></span> &nbsp <span >{1}</span> &nbsp<span style="color:#9F9F9F">{2}</span></li>
        <input type="text " class="hidden" name="tasid" value='{3}'>
        <input type="text " class="hidden" name="member_id" value='{4}'>
        """.format(member.name, status, last_edit,item.tasid, item.member_id)
        eles += ele
    eles += "</ul>"
    return mark_safe(eles)

@register.simple_tag
def bulid_review_list(tid):
    """构建任务审核对象"""
    task_assign_list = task_assign_db.query_task_assign_by_tid(tid)
    # task_review_list = task_review_db.query_task_reviewer_by_tid(tid)
    eles = """<ul>"""
    for item in task_assign_list:
        # 获取对象信息
        member = staff_db.query_staff_by_id(item.member_id_id)
        # 如果有记录表示已审核
        if item.is_finish:
            status = "通过"
            last_edit.last_edit.strftime("%Y-%m-%d")
        else:
            status = "审核中"
            last_edit = ''
            # 构建任务审核对象列表
        ele = """<li > <a  style="color:blue" href="task_review_record.html?tasid={0}">{1} &nbsp
                 <span style="color:red"> [ </span><span>{2}</span><span style="color:red"> ] 
                  </span></a> &nbsp<span style="color:#9F9F9F">{3}</span></li>
                  """.format(item.tasid, member.name, status, last_edit)
        eles += ele
    eles += "</ul>"
    return mark_safe(eles)


@register.simple_tag
def bulid_person_review_list(user_id,tid):
    """构建个人任务审核对象"""
    task_assign_list = task_assign_db.query_task_assign_by_tid(tid)
    eles = """<ul>"""
    for item in task_assign_list:
        # 获取对象信息
        member = staff_db.query_staff_by_id(item.member_id_id)
        # 根据用户sid和任务id获取审核
        task_review = task_review_db.query_task_reviewer_by_tid_sid(tid, user_id)
        # 获取任务最后一次审核记录
        last_review_record = task_review_record_db.query_task_review_record_last_by_tvid_and_tasid(task_review.tvid, item.tasid)
        # 获取任务提交记录
        last_commit_record = task_submit_record_db.query_last_submit_record(item.tasid)
        # 如果有记录表示已审核
        if last_review_record:
            is_review = "已审核"
            last_edit=last_review_record.create_time.strftime("%Y-%m-%d")
            if last_review_record.is_complete:
                status = "通过"
            else:
                status = '驳回'
        # 如果没有记录表示未审核
        else:
            is_review = "未审核"
            if last_commit_record:
                completion = last_commit_record.completion
                last_edit = last_commit_record.last_edit.strftime("%Y-%m-%d")
                status ="完成度："+str(completion) + "%"
            else:
                status = "进行中"
                last_edit = ''
            # 构建任务审核对象列表
        ele = """<li > <a  style="color:blue" href="task_review.html?tasid={0}">{1} &nbsp
                  <span >{2}</span> &nbsp<span style="color:red"> [ </span><span>{3}</span><span style="color:red"> ] 
                  </span></a> &nbsp<span style="color:#9F9F9F">{4}</span></li>
                  """.format(item.tasid,member.name, is_review, status,last_edit)
        eles += ele
    eles += "</ul>"
    return mark_safe(eles)


@register.simple_tag
def build_countdown_time(deadline):
    """构建截止时间"""
    now_time = datetime.now()
    left_time = deadline-now_time
    last_days = left_time.days
    if last_days < 0:
        last_days =0
    return last_days


@register.simple_tag
def build_record_tags_ele(tsid):
    """构建任务提交记录标签"""
    ele_list = ''
    record_tags = task_submit_tag_db.query_task_tag_by_tsid(tsid)
    for item in record_tags:
        if item.name:
            ele = "<span>{0};</span>".format(item.name)
            ele_list += ele
    return mark_safe(ele_list)

@register.simple_tag
def query_task_by_tid(tid):
    result_db = task_db.query_task_by_tid(tid)
    return result_db


@register.simple_tag
def query_task_attachment_by_tasid(tasid):
    tasid = int(tasid)
    result_db = task_assign_attach_db.query_task_assign_attach_by_tasid(tasid)
    return result_db


@register.simple_tag
def query_task_attachment_by_tid(tid):
    tid = int(tid)
    result_db = task_attachment_db.query_task_attachment_by_tid(tid)
    return result_db


@register.simple_tag
def query_submit_attachment_by_tsid(tsid):
    tsid = int(tsid)
    result_db = task_submit_attach_db.query_task_submit_attachment_by_tsid(tsid)
    return result_db