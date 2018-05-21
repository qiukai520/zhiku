from django import template
from django.utils.safestring import mark_safe
from task.server import *
# from task.server import task_db, task_cycle_db, staff_db, task_type_db, department_db, performence_db, task_assign_db,task_submit_record_db
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
    task_type_list = task_type_db.query_task_type_list()
    eles = ""
    for item in task_type_list:
        if selected == item.tpid:
            ele = """<option  selected=selected value={0}>{1}</option>""".format(item.tpid, item.name)
        else:
            ele = """<option value={0}>{1}</option>""".format(item.tpid, item.name)
        eles += ele
    return mark_safe(eles)


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
def change_to_task_type(ttid):
    """转化成任务类型"""
    task_type = task_type_db.query_task_type_by_id(ttid)
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
def change_to_task_finish_status(id):
    """获取任务完成状态"""
    finish_list = task_db.is_finish
    for item in finish_list:
        if int(item['id']) == id:
            return item['caption']

@register.simple_tag
def bulid_assign_member_list(tid):
    """构建指派对象"""
    task_assign_list = task_assign_db.query_task_assign_by_tid(tid)
    eles = """<ul>"""
    for item in task_assign_list:
        # 获取对象信息
        member = staff_db.query_staff_by_id(item.member_id)
        # 获取任务提交记录
        last_commit_record = task_submit_record_db.query_last_submit_record(item.tasid)
        if last_commit_record:
            completion = last_commit_record.completion
            last_edit = last_commit_record.last_edit
            if completion:
                status = completion
        else:
            status = "进行中"
            last_edit = ''
        # 构建指派对象列表
        ele = """<li data-toggle="modal" onclick="MemberAssignShow(this)"><span class="member_name"  >{0}</span>  &nbsp
        <span >{1}</span> &nbsp<span>{2}</span></li><input type="text " class="hidden" name="tasid" value='{3}'>
        <input type="text " class="hidden" name="member_id" value='{4}'>
        """.format(member.name, status, last_edit,item.tasid, item.member_id)
        eles += ele
    eles += "</ul>"
    return mark_safe(eles)

