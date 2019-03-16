import time
from datetime import datetime
from datetime import timedelta
from django import template
from django.utils.safestring import mark_safe
from task.server import *
from personnel.server import *
from task.utils import getMonthFirstDayAndLastDay

register = template.Library()
@register.simple_tag
def build_department_ele():
    """构建部门下拉框"""
    dp_list = department_db.query_department_list()
    eles = ""
    for item in dp_list:
        ele = """<option value={0} >{1}</option>""".format(item.id, item.department)
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_staff_ele(dpid=0):
    """构建员工下拉框"""
    if dpid != ''and 0:
         # 根据部门获取员工
        dp_list = staff_db.query_staff_by_department_id(dpid)
    else:
        dp_list = staff_db.query_staff_list()
    eles = ""
    for item in dp_list:
        ele = """<option value={0} >{1}</option>""".format(item.sid, item.name)
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
    way_list = task_map_db.execute_way
    eles = ""
    for item in way_list:
      ele = """<option value={0}>{1}</option>""".format(item["execute_way"], item["caption"])
      eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_task_cycle_ele():
    """构建任务周期下拉框"""
    way_list = task_map_db.cycle_choice
    eles = ""
    for item in way_list:
      ele = """<option value={0}>{1}</option>""".format(item["id"], item["caption"])
      eles += ele
    return mark_safe(eles)



# @register.simple_tag
# def build_task_cycle_ele():
#     """构建任务周期下拉框"""
#     cycle_list = task_cycle_db.query_task_cycle_list()
#     eles = ""
#     for item in cycle_list:
#         ele = """<option value={0}>{1}</option>""".format(item.tcid, item.name)
#         eles += ele
#     return mark_safe(eles)


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
def build_task_assign_status_filter(selected):
    """构建指派任务选择框"""
    selected = int(selected)
    task_assign_is_finish = task_assign_db.is_finish
    eles = ""
    for item in task_assign_is_finish:
        if selected == item['id']:
            ele = """<option selected=selected value={0}>{1}</option>""".format(item['id'], item['caption'])
        else:
            ele = """<option value={0}>{1}</option>""".format(item['id'], item['caption'])
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
def build_task_review_ele(tmid):
    """构建任务标签"""
    ele_list = ''
    task_review_ids = task_review_db.query_task_reviewer_by_tmid(tmid).order_by("follow")
    if task_review_ids:
        for item in task_review_ids:
            staff = staff_db.query_staff_by_id(item.sid_id)
            if staff:
                ele = "<span>{0};</span>".format(staff.name)
                ele_list += ele
    else:
        ele = "<span>{0};</span>".format("暂未指定")
        ele_list += ele
    return mark_safe(ele_list)

@register.simple_tag
def build_task_period_review_ele(tpid):
    """构建周期任务标签"""
    ele_list = ''
    task_review_ids = task_period_review_db.query_task_reviewer_by_tpid(tpid).order_by("follow")
    if task_review_ids:
        for item in task_review_ids:
            staff = staff_db.query_staff_by_id(item.sid_id)
            if staff:
                ele = "<span>{0};</span>".format(staff.name)
                ele_list += ele
    else:
        ele = "<span>{0};</span>".format("暂未指定")
        ele_list += ele
    return mark_safe(ele_list)


@register.simple_tag
def build_task_type_ele(selected=None):
    """构建任务类型选择框"""
    if selected:
        selected = int(selected)
    task_type_list = task_type_db.query_task_type_list()
    eles = ""
    for item in task_type_list:
        if item.tpid == selected:
            ele = """<option selected=selected value={0}>{1}</option>""".format(item.tpid, item.name)
        else:
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
def change_to_review_result(result):
    print(result)
    result_choice=task_review_result_db.result_choice
    for item in result_choice:
        if int(item["id"]) == result:
            return item["caption"]


@register.simple_tag
def change_to_task_way(team_id):
    task_way = task_map_db.task_way
    for item in task_way:
        if int(item["id"]) == team_id:
            return item["caption"]

@register.simple_tag
def query_task_way_by_tmid(tmid):
    task_map_obj = task_map_db.query_task_by_tmid(tmid)
    if task_map_obj:
        caption = change_to_task_way(task_map_obj.team)
        return caption
    return "未知"


@register.simple_tag
def change_to_task_type(tpid):
    """转化成任务类型"""
    if tpid:
        task_type = task_type_db.query_task_type_by_id(tpid)
        return task_type.name
    return ""

@register.simple_tag
def change_to_staff(sid):
    """获取根据id员工"""
    issuer = staff_db.query_staff_by_id(sid)
    if issuer:
        name = issuer.name
    else:
        name = "人工录入"
    return name


@register.simple_tag
def change_to_department(dpid):
    """根据id获取部门"""
    depart = department_db.query_department_by_id(dpid)
    if depart:
        name = depart.department
    else:
        name = ""
    return name

@register.simple_tag
def change_to_task_cycle(tcid):
    """获取任务周期"""
    task_cycle = task_period_db.cycle_choice
    if tcid:
        for item in task_cycle:
            if int(item["id"]) == tcid:
                return item['caption']
    else:
        return "未知"


# @register.simple_tag
# def change_to_task_assign_status(id):
#     """获取任务指派状态"""
#     assign_list = task_db.is_assign
#     for item in assign_list:
#         if int(item["iaid"]) == id:
#             return item["caption"]

@register.simple_tag
def change_to_task_status(id):
    """获取任务状态"""
    status_list = task_map_db.task_status
    for item in status_list:
        if int(item["id"]) == id:
            return item['caption']

@register.simple_tag
def change_to_task_assign_finish(is_finish):
    is_finish_list = task_assign_db.is_finish
    for item in is_finish_list:
        if int(item["id"]) == is_finish:
            return item['caption']


@register.simple_tag
def change_to_task_assign_status(status):
    status_list = task_assign_db.status
    for item in status_list:
        if int(item["id"]) == status:
            return item['caption']

@register.simple_tag
def change_to_task_perfomance(pid):
    """获取任务绩效"""
    performance = performence_db.query_performence_by_pid(pid)
    return performance.name


@register.simple_tag
def change_to_task_finish_status(id):
    """获取任务完成状态"""
    finish_list = task_map_db.is_finish
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
def bulid_assign_member_list(tmid,deadline):
    """构建指派对象"""
    task_assign_list = task_assign_db.query_task_assign_by_tmid(tmid)
    eles = """<ul>"""
    for item in task_assign_list:
        # 获取对象信息
        member = staff_db.query_staff_by_id(item.member_id_id)
        if member:
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
            ele = """<li data-toggle="modal" onclick="MemberAssignShow(this)"><span style="color: #1ab394" class="member_name"  >{0}</span>  &nbsp
            <span style="color: #1ab394" class="glyphicon glyphicon-plus plus " ></span> &nbsp <span >{1}</span> &nbsp<span style="color:#9F9F9F">{2}</span></li>
            <input type="text " class="hidden" name="tasid" value='{3}'>
            <input type="text " class="hidden" name="member_id" value='{4}'>
             <input type="text " class="hidden" name="deadline" value='{5}'>
            """.format(member.name, status, last_edit,item.tasid, item.member_id, deadline)
            eles += ele
    eles += "</ul>"
    return mark_safe(eles)

@register.simple_tag
def bulid_review_list(tmid):
    """构建任务审核对象"""
    path = "center/record"
    task_assign_list = task_assign_db.query_task_assign_by_tmid(tmid)
    # task_review_list = task_review_db.query_task_reviewer_by_tid(tid)
    eles = """<ul>"""
    for item in task_assign_list:
        # 获取对象信息
        member = staff_db.query_staff_by_id(item.member_id_id)
        if member:
            # 如果有记录表示已审核
            if item.is_finish:
                status = "通过"
                last_edit=item.last_edit.strftime("%Y-%m-%d")
            else:
                status = "审核中"
                last_edit = ''
                # 构建任务审核对象列表
            ele = """<li > <a  style="color:#1ab394" href="{0}?tasid={1}">{2} &nbsp
                     <span style="color:red"> [ </span><span>{3}</span><span style="color:red"> ] 
                      </span></a> &nbsp<span style="color:#9F9F9F">{4}</span></li>
                      """.format(path,item.tasid, member.name, status, last_edit)
            eles += ele
    eles += "</ul>"
    return mark_safe(eles)


@register.simple_tag
def bulid_person_review_list(user_id,tmid):
    """构建个人任务审核对象"""
    path = "reviews/review"
    task_assign_list = task_assign_db.query_task_assign_by_tmid(tmid)
    eles = """<ul>"""
    for item in task_assign_list:
        # 获取对象信息
        member = staff_db.query_staff_by_id(item.member_id_id)
        if member:
            # 根据用户sid和任务id获取审核
            task_review = task_review_db.query_task_reviewer_by_tid_sid(tmid, user_id)
            # 查看是否为次序审核,大于0则为次序审核
            flag = True
            if task_review.follow > 1:
                pre_follow = task_review.follow
                pre_obj = task_review_db.query_task_reviewer_by_tid_follow(tmid,pre_follow)
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
                ele = """<li > <a  style="color: #1ab394" href="{0}?tasid={1}">{2} &nbsp
                          <span >{3}</span> &nbsp<span style="color:red"> [ </span><span>{4}</span><span style="color:red"> ] 
                          </span></a> &nbsp<span style="color:#9F9F9F">{5}</span></li>
                          """.format(path,item.tasid,member.name, is_review, status,last_edit)
            else:
                ele = """<li ><span style="color: #1ab394" >{0}</span> &nbsp<span style="color:red"> [ </span><span>上一审核人还未审核</span><span style="color:red"> ] 
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
    if tid:
        tid = int(tid)
        result_db = task_db.query_task_by_tid(tid)
        return result_db
    return ""

@register.simple_tag
def query_task_map_by_tmid(tmid):
    result_db = task_map_db.query_task_by_tmid(tmid)
    return result_db

@register.simple_tag
def query_task_by_tmid(tmid):
    task_map_obj = task_map_db.query_task_by_tmid(tmid)
    if task_map_obj:
        task_obj = task_db.query_task_by_tid(task_map_obj.tid_id)
        return task_obj
    return ''

@register.simple_tag
def query_task_attachment_by_tasid(tasid):
    """获取指派任务的附件"""
    tasid = int(tasid)
    result_db = task_assign_attach_db.query_task_assign_attach_by_tasid(tasid)
    return result_db


@register.simple_tag
def query_task_attachment_by_tid(tid):
    if tid:
        tid = int(tid)
        result_db = task_attachment_db.query_task_attachment_by_tid(tid)
        return result_db
    return ''


@register.simple_tag
def query_task_map_attachment_by_tmid(tmid):
    if tmid:
        tmid = int(tmid)
        result_db = task_map_att_db.query_attachment_by_tmid(tmid)
        return result_db
    return ''


@register.simple_tag
def query_task_period_attachment_by_tpid(tpid):
    if tpid:
        tpid = int(tpid)
        result_db = task_period_att_db.query_attachment_by_tpid(tpid)
        return result_db
    return []

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
def fetch_task_review_status(tasid,sid):
    result_db = task_review_result_db.query_task_review_by_tasid_sid(tasid,sid)
    if result_db:
        choice_list = task_review_result_db.result_choice
        for item in choice_list:
            if item["id"] == result_db.result:
                return item['caption']

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
def build_task_map_tags_list(tmid):
    """构建任务指派标签列表"""
    ele_list = ''
    record_tags = task_map_tag_db.query_tag_by_tmid(tmid)
    for item in record_tags:
        if item.name:
            ele = "<li><a><i class='fa fa-tag'></i> {0}</a></li>".format(item.name)
            ele_list += ele
    return mark_safe(ele_list)

@register.simple_tag
def build_task_period_tags_list(tpid):
    """构建周期任务标签列表"""
    ele_list = ''
    record_tags = task_period_tag_db.query_tag_by_tpid(tpid)
    for item in record_tags:
        if item.name:
            ele = "<li><a><i class='fa fa-tag'></i> {0}</a></li>".format(item.name)
            ele_list += ele
    return mark_safe(ele_list)

@register.simple_tag
def build_task_assign_tags_list(tasid):
    """构建任务标签列表"""
    ele_list = ''
    record_tags = task_assign_tag_db.query_task_assign_tag_by_tasid(tasid)
    for item in record_tags:
        if item.name:
            ele = "<li><a><i class='fa fa-tag'></i> {0}</a></li>".format(item.name)
            ele_list += ele
    return mark_safe(ele_list)



@register.simple_tag
def fetch_task_assign_member(tmid):
    """获取任务成员"""
    # 指派路径
    task_assign_list = task_assign_db.query_task_assign_by_tmid(tmid)
    eles = ''
    if task_assign_list:
        path = "/task/review/center/record"
        for item in task_assign_list:
            member = staff_db.query_staff_by_id(item.member_id_id)
            if member:
                ele = "<a href='{0}?tasid={1}'>{2};&nbsp</a>".format(path,item.tasid, member.name)
                eles+= ele
    else:
        path = "/task/map/edit"
        ele = "<span>暂未指派</span> &nbsp<a href='{0}?tmid={1}'>去指派</a>".format(path,tmid)
        eles += ele
    return mark_safe(eles)


@register.simple_tag
def fetch_team_member(tmid):
    """获取团队成员"""
    task_assign_list = task_assign_db.query_task_assign_by_tmid(tmid)
    eles = ''
    if task_assign_list:
        for item in task_assign_list:
            member = staff_db.query_staff_by_id(item.member_id_id)
            if member:
                ele = "<span>{0};&nbsp</span>".format(member.name)
                eles+= ele
    else:
        ele = "<span>无</span> &nbsp"
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def fetch_task_period_assign_member(tpid):
    """获取任务成员"""
    # 指派路径
    task_assign_list = task_period_assigner_db.query_task_assigner_by_tpid(tpid)
    eles = ''
    if task_assign_list:
        for item in task_assign_list:
            member = staff_db.query_staff_by_id(item.member_id_id)
            if member:
                ele = "<span>{0};&nbsp</span>".format(member.name)
                eles+= ele
    else:
        ele = "<span>暂未指派</span> &nbsp"
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def fetch_review_follow(tmid):
    """获取任务审核次序"""
    task_review = task_review_db.query_task_reviewer_by_tmid(tmid)
    if task_review:
        if task_review[0].follow:
            result = '是'
        else:
            result = '否'
    else:
        result = "未指定"
    return result


@register.simple_tag
def fetch_task_period_review_follow(tpid):
    """获取任务审核次序"""
    task_review = task_period_review_db.query_task_reviewer_by_tpid(tpid)
    if task_review:
        if task_review[0].follow:
            result = '是'
        else:
            result = '否'
    else:
        result = "未指定"
    return result

@register.simple_tag
def fetch_task_map_record(tid):
    query_set = task_map_db.query_task_by_tid(tid)
    result_db = query_set.order_by("-tmid")
    return result_db


@register.simple_tag
def build_task_progress(tmid):
    """计算任务进度
    设定完成占80%
    审核通过占20%
    """
    progress_rate = 80
    finish_rate = 20
    task_assign_list = task_assign_db.query_task_assign_by_tmid(tmid)
    length = len(task_assign_list)
    if length:
        total_progress = 0
        total_finish = 0
        for item in task_assign_list:
            if item.progress:
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
def fetch_task_submit_record(tmid):
    """获取任务提交记录"""
    task_assign_list = task_assign_db.query_task_assign_by_tmid(tmid)
    tasid_list = []
    for item in task_assign_list:
        tasid_list.append(item.tasid)
    task_submit_record = task_submit_record_db.query_submit_by_tasid_list(tasid_list)
    return task_submit_record


@register.simple_tag
def fetch_task_assign_member_by_tasid(tasid,show=1):
    path="/task/review/center/record"
    task_assign_obj = task_assign_db.query_task_assign_by_tasid(tasid)
    task_assign_obj = task_assign_obj.first()
    staff_obj = staff_db.query_staff_by_id(task_assign_obj.member_id_id)
    if staff_obj:
        if show:
            ele = "<a href='{0}?tasid={1}'>{2}&nbsp</a>".format(path,tasid, staff_obj.name)
        else:
            ele ="<span>{0}</span>".format(staff_obj.name)
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
def fetch_task_assing_list(tmid):
    """获取任务成员列表"""
    task_assign_list = task_assign_db.query_task_assign_by_tmid(tmid)
    return task_assign_list


@register.simple_tag
def fetch_task_review_result(tasid):
    """获取任务审核记录"""
    if tasid:
        task_review_result = task_review_record_db.query_task_review_record_list_by_tasid(tasid)
        return task_review_result

@register.simple_tag
def fetch_task_review(tvid):
    if tvid:
        task_review = task_review_db.query_task_reviewer_by_tvid(tvid)
        return task_review

@register.simple_tag
def fetch_assign_finish_status(status):
    """获取任务成员审核情况"""
    if status == 1:
        status = "已通过"
    else:
        status = '待审核'
    return status


@register.simple_tag
def count_personal_total_task(sid, startMonth, endMonth):
    """获取单月个人任务总数"""
    first_day,last_day = getMonthFirstDayAndLastDay(startMonth, endMonth)
    total = task_assign_db.count_personal_total_task(sid, first_day, last_day)
    return total

@register.simple_tag
def count_personal_finish_task(sid, startMonth, endMonth):
    """获取单月个人完成总数"""
    first_day, last_day = getMonthFirstDayAndLastDay(startMonth, endMonth)
    total = task_assign_db.count_personal_finish_task(sid, first_day, last_day)
    return total

@register.simple_tag
def count_team_total_task(sid, startMonth, endMonth):
    """获取单月团队任务总数"""
    first_day,last_day = getMonthFirstDayAndLastDay(startMonth,endMonth)
    total = task_assign_db.count_team_total_task(sid,first_day,last_day)
    return total

@register.simple_tag
def count_team_finish_task(sid, startMonth, endMonth):
    """获取单月团队完成总数"""
    first_day,last_day = getMonthFirstDayAndLastDay(startMonth, endMonth)
    total = task_assign_db.count_team_finish_task(sid,first_day,last_day)
    return total





