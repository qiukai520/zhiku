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
    selected = int(selected)
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
    if record_tags:
        for item in record_tags:
            if item.name:
                ele = "<span>{0};</span>".format(item.name)
                ele_list += ele
    else:
        ele = "<span>{0};</span>".format("暂无")
        ele_list += ele
    return mark_safe(ele_list)

@register.simple_tag
def build_task_review_ele(tid):
    """构建任务标签"""
    ele_list = ''
    task_review_ids = task_review_db.query_task_reviewer_by_tid(tid).order_by("follow")
    if task_review_ids:
        for item in task_review_ids:
            staff = staff_db.query_staff_by_id(item.sid_id)
            if staff.name:
                ele = "<span>{0};</span>".format(staff.name)
                ele_list += ele
    else:
        ele = "<span>{0};</span>".format("暂未指定")
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
def change_to_task_way(team_id):
    task_way = task_db.task_way
    for item in task_way:
        if int(item["id"]) == team_id:
            return item["caption"]


@register.simple_tag
def change_to_task_type(tpid):
    """转化成任务类型"""
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
def bulid_assign_member_list(tid,deadline):
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
         <input type="text " class="hidden" name="deadline" value='{5}'>
        """.format(member.name, status, last_edit,item.tasid, item.member_id, deadline)
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
        # 查看是否为次序审核,大于0则为次序审核
        flag = True
        if task_review.follow > 1:
            pre_follow = task_review.follow
            pre_obj = task_review_db.query_task_reviewer_by_tid_follow(tid,pre_follow)
            last_review_record = task_review_record_db.query_task_review_record_last_by_tvid_and_tasid(pre_obj.tvid,
                                                                                                       item.tasid)
            if last_review_record:
                if last_review_record.is_complete == 0:
                    flag = False
            else:
                flag = False
        if flag:
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
        else:
            ele = """<li ><span style="color:blue" >{0}</span> &nbsp<span style="color:red"> [ </span><span>上一审核人还未审核</span><span style="color:red"> ] 
                                 </span></li>
                                 """.format(member.name)
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
    """获取指派任务的附件"""
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
    """获取任务提交记录附件"""
    tsid = int(tsid)
    result_db = task_submit_attach_db.query_task_submit_attachment_by_tsid(tsid)
    return result_db


@register.simple_tag
def fetch_completion_by_tasid(tasid):
    """获取指派任务的完成度"""
    last_commit_record = task_submit_record_db.query_last_submit_record(tasid)
    if last_commit_record:
        completion = last_commit_record.completion
        last_edit = last_commit_record.last_edit.strftime("%Y-%m-%d")
        if completion:
            completion = completion
    else:
        completion = 0
    return completion


@register.simple_tag
def build_task_tags_list(tid):
    """构建任务标签列表"""
    ele_list = ''
    record_tags = task_tag_db.query_task_tag_by_tid(tid)
    for item in record_tags:
        if item.name:
            ele = "<li><a><i class='fa fa-tag'></i> {0}</a></li>".format(item.name)
            ele_list += ele
    return mark_safe(ele_list)

@register.simple_tag
def fetch_task_assing_member(tid):
    """获取任务成员"""
    task_assign_list = task_assign_db.query_task_assign_by_tid(tid)
    eles = ''
    if task_assign_list:
        for item in task_assign_list:
            member = staff_db.query_staff_by_id(item.member_id_id)
            ele = "<a href='task_review_record.html?tasid={0}'>{1};&nbsp</a>".format(item.tasid, member.name)
            eles+= ele
    else:
        ele = "<span>暂未指派</span> &nbsp<a href='task_assign_center.html'>去指派</a>"
        eles += ele
    return mark_safe(eles)


@register.simple_tag
def fetch_review_follow(tid):
    """获取任务审核次序"""
    task_review = task_review_db.query_task_reviewer_by_tid(tid)
    if task_review:
        if task_review[0].follow:
            result = '是'
        else:
            result = '否'
    else:
        result = "未指定"
    return result


@register.simple_tag
def build_task_progress(tid):
    """计算任务进度
    设定完成占80%
    审核通过占20%
    """
    progress_rate = 80
    finish_rate = 20
    task_assign_list = task_assign_db.query_task_assign_by_tid(tid)
    length = len(task_assign_list)
    if length:
        total_progress = 0
        total_finish = 0
        for item in task_assign_list:
            total_progress += item.progress
            total_finish += item.is_finish
        if total_progress > 0:
            progress_score = total_progress/(length*100)*progress_rate
        else:
            progress_score = 0
        if total_finish > 0:
            finish_score = total_finish/length*finish_rate
        else:
            finish_score = 0
        completion = progress_score+finish_score
    else:
        completion = 0
    return int(completion)


@register.simple_tag
def fetch_task_submit_record(tid):
    """获取任务提交记录"""
    task_assign_list = task_assign_db.query_task_assign_by_tid(tid)
    tasid_list = []
    for item in task_assign_list:
        tasid_list.append(item.tasid)
    task_submit_record = task_submit_record_db.query_submit_by_tasid_list(tasid_list)
    return task_submit_record


@register.simple_tag
def fetch_task_assign_member_by_tasid(tasid):
    task_assign_obj = task_assign_db.query_task_assign_by_tasid(tasid)
    staff_obj = staff_db.query_staff_by_id(task_assign_obj.member_id_id)
    ele = "<a href='task_review_record.html?tasid={0}'>{1}&nbsp</a>".format(tasid, staff_obj.name)
    return mark_safe(ele)


@register.simple_tag
def calculate_past_days(time):
    """计算消息来自多少天前"""
    now_time = datetime.now()
    del_time = now_time.date() - time.date()
    del_day = del_time.days
    if del_day == 0:
        date = '今天'
    else:
        date = str(del_day) + '天前'
    return date


@register.simple_tag
def calculate_past_time(time):
    """计算消息来自什么时候具体到分钟"""
    now_time = datetime.now()
    del_time = now_time.date() - time.date()
    del_day = del_time.days
    if del_day == 0:
        del_seconds = int(now_time.timestamp()-time.timestamp())
        if del_seconds> 60:
             del_minute = int(del_seconds/60)
             if del_minute > 60:
                 del_hour = int(del_minute/60)
                 time = str(del_hour)+'小时'
             else:
                 time = str(del_minute)+'分钟'
        else:
            time="1分钟"
    else:
        time = str(del_day) + '天'
    return time


@register.simple_tag
def fetch_task_assing_list(tid):
    """获取任务成员列表"""
    task_assign_list = task_assign_db.query_task_assign_by_tid(tid)
    return task_assign_list


@register.simple_tag
def fetch_assign_finish_status(status):
    """获取任务成员审核情况"""
    if status == 1:
        status = "已通过"
    else:
        status = '待审核'
    return status










