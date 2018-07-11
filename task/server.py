from django.db import connection

from .models import *


class StaffDB(object):
    """员工表"""

    def query_staff_list(self):
        result_db = Staff.objects.filter().all()
        return result_db

    def query_staff_by_id(self, sid):
        result_db = Staff.objects.filter(sid=sid).first()
        return result_db

    def query_staff_by_department_id(self, department_id):
        result_db = Staff.objects.filter(department=department_id).all()
        return result_db


class DepartmentDB(object):
    """部门表"""
    def query_department_list(self):
        result_db = Department.objects.filter().all()
        return result_db


class PerformenceDB(object):
    """绩效表"""
    def query_performence_list(self):
        result_db = Performemce.objects.filter().all().order_by("-pid")
        return result_db

    def query_performence_by_pid(self, pid):
        result_db = Performemce.objects.filter(pid=pid).first()
        return result_db

    def insert_performence(self, modify_info):
        is_exists = Performemce.objects.filter(name=modify_info['name'])
        if is_exists:
            raise Exception('绩效已存在')
        Performemce.objects.create(**modify_info)

    def update_performence(self, modify_info):
        Performemce.objects.filter(pid=modify_info['pid']).update(**modify_info)

    def mutil_delete_performence(self, id_list):
        Performemce.objects.filter(pid__in=id_list).delete()


class TaskDB(object):
    """任务表列表"""
    # 任务状态
    task_status = (
        {"id": 1, "caption": "启动"},
        {"id": 2, "caption": "暂停"},
        {"id": 3, "caption": "终止"},
    )
    # 执行方式
    execute_way = (
        {"execute_way": 0, "caption": "并行执行"},
        {"execute_way": 1, "caption": "次序执行"},
    )
    # 是否指派
    is_assign = (
        {"iaid": 0, "caption": "未指派"},
        {"iaid": 1, "caption": "已指派"}

    )
    # 是否完成
    is_finish = (
        {"id": 0, "caption": "未完成"},
        {"id": 1, "caption": "已完成"}
    )

    def insert_task(self, modify_info):
        task_sql = """insert into task(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        task_sql = task_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(task_sql, modify_info)
        tid = cursor.lastrowid
        return tid

    def update_task(self, modify_info):
        Task.objects.filter(tid=modify_info['tid']).update(**modify_info)

    def query_task_lists(self):
        result_db = Task.objects.filter().all().order_by("-tid")
        return result_db

    def query_task_by_is_assign(self):
        result_db=Task.objects.filter(is_assign=1).all()
        return result_db

    def query_task_assign_lists(self):
        result_db = Task.objects.filter(is_assign=1).all().order_by("-tid")
        return result_db

    def query_task_by_tid(self, tid):
        result_db = Task.objects.filter(tid=tid).first()
        return result_db

    def query_task_by_tids(self,tids):
        result_db = Task.objects.filter(tid__in=tids).all()
        return result_db

    def query_task_by_type(self, type_id):
        result_db = Task.objects.filter(type_id=type_id).all()
        return result_db

    def query_task_by_issuer_id(self, issuer_id):
        result_db = Task.objects.filter(issuer_id=issuer_id).first()
        return result_db

    def multi_delete_task(self, id_list):
        Task.objects.filter(tid__in=id_list).delete()

    def update_task_status_by_tid(self, tid,modify_info):
        Task.objects.filter(tid=tid).update(**modify_info)


class TaskCycleDB(object):
    """任务周期表"""
    def query_task_cycle_list(self):
        result_db = TaskCycle.objects .filter().all()
        return result_db

    def query_task_cycled_by_tcid(self, tcid):
        result_db = TaskCycle.objects.filter(tcid=tcid).first()
        return result_db


class TaskTypeDB(object):
    """任务类型表"""
    def query_task_type_list(self):
        result_db = TaskType.objects.filter().all()
        return result_db

    def insert_task_type(self, modify_info):
        TaskType.objects.create(**modify_info)

    def query_task_type_by_id(self, tpid):
        result_db = TaskType.objects.filter(tpid=tpid).first()
        return result_db

    def update_task_type(self, modify_info):
        TaskType.objects.update(**modify_info)

    def mutil_delete_task_type(self,ids):
        TaskType.objects.filter(tpid__in=ids).delete()


class TaskAttachmentDB(object):
    """任务附件表"""
    def query_task_attachment_list(self):
        result_db = TaskAttachment.objects.filter().all()
        return result_db

    def query_task_attachment_by_tid(self, tid):
        result_db = TaskAttachment.objects.filter(tid_id=tid).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            TaskAttachment.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            TaskAttachment.objects.filter(tamid=item['tamid']).update(**item)

    def mutil_delete_task_attachment(self, id_list):
        TaskAttachment.objects.filter(tamid__in=id_list).delete()

    def multi_delete_attach_by_tid(self,id_list):
        TaskAttachment.objects.filter(tid_id__in=id_list).filter().delete()

    def delete_task_attachment(self,tamid):
        TaskAttachment.objects.filter(tamid=tamid).delete()


class TaskTagDB(object):
    """任务标签"""
    def mutil_insert_tag(self, modify_info_list):
        for item in modify_info_list:
            is_exists = TaskTag.objects.filter(tid_id=item['tid_id'], name=item['name'])
            if is_exists:
                continue
            TaskTag.objects.create(**item)

    def mutil_update_tag(self, modify_info_list):
        for item in modify_info_list:
            TaskTag.objects.filter(ttid=item['ttid']).update(**item)

    def mutil_delete_tag(self, id_list):
        TaskTag.objects.filter(ttid__in=id_list).delete()

    def mutil_delete_tag_by_tid(self, id_list):
        TaskTag.objects.filter(tid_id__in=id_list).delete()

    def query_task_tag_by_tid(self, tid):
        result_db = TaskTag.objects.filter(tid_id=tid).all()
        return result_db


class TaskReviewDB(object):
    """任务审核人"""
    def mutil_insert_reviewer(self, modify_info_list):
        for item in modify_info_list:
            TaskReview.objects.create(**item)

    def query_task_reviewer_by_tid(self,tid):
        result_db = TaskReview.objects.filter(tid_id=tid).all()
        return result_db

    def query_task_reviewer_by_sid(self,sid):
        result_db = TaskReview.objects.filter(sid_id=sid).all()
        return result_db

    def query_task_reviewer_by_tvid(self,tvid):
        result_db = TaskReview.objects.filter(tvid=tvid).first()
        return result_db

    def query_task_reviewer_by_tid_sid(self, tid, sid):
        result_db = TaskReview.objects.filter(tid_id=tid, sid_id=sid).first()
        return result_db

    def mutil_update_reviewer(self, modify_info):
        for item in modify_info:
            TaskReview.objects.filter(tid_id=item['tid'], sid_id=item['sid']).update(**item)

    def mutil_delete_reviewer(self, id_list):
        TaskReview.objects.filter(tvid__in=id_list).delete()

    def mutil_delete_reviewer_by_tid(self,tid_list):
        TaskReview.objects.filter(tid_id__in=tid_list).delete()


class TaskAssignDB(object):
    """任务指派表"""
    def mutil_insert_task_assign(self, modify_info_list):
        for item in modify_info_list:
            is_exist = TaskAssign.objects.filter(tid_id=item['tid_id'], member_id_id=item['member_id_id'])
            if is_exist:
                result_db = staff_db.query_staff_by_id(item['member_id_id'])
                raise Exception('%s已指派过该任务'%(result_db.name))
            TaskAssign.objects.create(**item)

    def update_task_assign(self,modify_info):
        TaskAssign.objects.filter(tasid=modify_info["tasid"]).update(**modify_info)

    def update_finish_status(self,is_finish):
        TaskAssign.objects.update(is_finish=is_finish)

    def query_task_assign_by_tid(self, tid):
        result_db = TaskAssign.objects.filter(tid=tid).all()
        return result_db

    def query_task_assign_by_tasid(self, tasid):
        result_db = TaskAssign.objects.filter(tasid=tasid).all()
        return result_db

    def query_task_assign_by_member_id(self, member_id):
        result_db = TaskAssign.objects.filter(member_id=member_id).all()
        return result_db


class TaskSubmitRecordDB(object):
    """任务提交记录表"""

    def query_last_submit_record(self, tasid):
        result_db = TaskSubmitRecord.objects.filter(tasid_id=tasid).last()
        return result_db

    def query_submit_by_tasid(self, tasid):
        result_db = TaskSubmitRecord.objects.filter(tasid_id=tasid).all().order_by("-tsid")
        return result_db

    def insert_task_submit_record(self,modify_info):
        submit_record_sql = """insert into task_submit_record(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        submit_record_sql = submit_record_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(submit_record_sql, modify_info)
        tsid = cursor.lastrowid
        return tsid


class TaskSubmitAttachmentDB(object):
    """任务附件表"""
    def query_task_submit_attachment_list(self):
        result_db = TaskSubmitAttachment.objects.filter().all()
        return result_db

    def query_task_submit_attachment_by_tsid(self,tsid):
        result_db = TaskSubmitAttachment.objects.filter(tsid=tsid).all()
        return result_db

    def mutil_insert_attachment(self, modify_info_list):
        for item in modify_info_list:
            TaskSubmitAttachment.objects.create(**item)

    def mutil_update_attachment(self, modify_info_list):
        for item in modify_info_list:
            TaskSubmitAttachment.objects.filter(tsaid=item['tsaid']).update(**item)

    def mutil_delete_task_attachment(self, id_list):
        TaskSubmitAttachment.objects.filter(tsaid__in=id_list).delete()

    def multi_delete_attach_by_tsid(self,id_list):
        TaskSubmitAttachment.objects.filter(tsid__in=id_list).filter().delete()

    def delete_task_attachment(self,tsaid):
        TaskSubmitAttachment.objects.filter(tsaid=tsaid).delete()


class TaskSubmitTagDB(object):
    """任务标签"""
    def mutil_insert_tag(self, modify_info_list):
        for item in modify_info_list:
            is_exists = TaskSubmitTag.objects.filter(tsid=item['tsid'], name=item['name'])
            if is_exists:
                continue
            TaskSubmitTag.objects.create(**item)

    def mutil_update_tag(self, modify_info_list):
        for item in modify_info_list:
            TaskSubmitTag.objects.filter(tstid=item['tstid']).update(**item)

    def mutil_delete_tag(self, id_list):
        TaskSubmitTag.objects.filter(tstid__in=id_list).delete()

    def mutil_delete_tag_by_tsid(self, id_list):
        TaskSubmitTag.objects.filter(tsid__in=id_list).delete()

    def query_task_tag_by_tsid(self, tsid):
        result_db = TaskSubmitTag.objects.filter(tsid=tsid).all()
        return result_db


class TaskAssignTagDB(object):
    """任务分配表"""
    def mutil_insert_assign_tag(self, modify_info_list):
        for item in modify_info_list:
            is_exists = TaskAssignTag.objects.filter(tasid_id=item['tasid_id'], name=item['name']).first()
            if is_exists:
                continue
            TaskAssignTag.objects.create(**item)

    def query_task_assign_tag_by_tasid(self, tasid):
        result_db = TaskAssignTag.objects.filter(tasid_id=tasid).all()
        return result_db

    def mutil_update_assign_tag(self,modify_info_list):
        for item in modify_info_list:
            TaskAssignTag.objects.filter(tatid_id=item['tatid']).update(**item)

    def mutil_delete_tag(self, id_list):
        TaskAssignTag.objects.filter(tatid__in=id_list).delete()


class TaskAssignAttachDB(object):
    """任务分配附件表"""
    def mutil_insert_assign_attach(self, modify_info_list):
        for item in modify_info_list:
            TaskAssignAttach.objects.create(**item)

    def query_task_assign_attach_by_tasid(self ,tasid):
        result_db = TaskAssignAttach.objects.filter(tasid_id=tasid).all()
        return result_db

    def mutil_update_assign_attach(self,modify_info_list):
        for item in modify_info_list:
            TaskAssignAttach.objects.filter(taaid_id=item['taaid_id']).update(**item)

    def mutil_delete_attach(self, id_list):
        TaskAssignAttach.objects.filter(taaid__in=id_list).delete()


class TaskReviewRecordDB(object):
    """任务审核记录表"""
    def query_task_review_record_last_by_tvid_and_tasid(self, tvid,tasid):
        result_db = TaskReviewRecord.objects.filter(tvid_id=tvid, tasid_id=tasid).last()
        return result_db

    def query_task_review_record_list_by_tvid_and_tasid(self,tvid,tasid):
        result_db = TaskReviewRecord.objects.filter(tvid_id=tvid, tasid_id=tasid).all().order_by("-trrid")
        return result_db

    def insert_review_record(self, modify_info):
        TaskReviewRecord.objects.create(**modify_info)


department_db = DepartmentDB()
staff_db = StaffDB()
task_db = TaskDB()
task_cycle_db = TaskCycleDB()
task_type_db = TaskTypeDB()
task_attachment_db = TaskAttachmentDB()
task_tag_db = TaskTagDB()
task_review_db = TaskReviewDB()
performence_db = PerformenceDB()
task_assign_db = TaskAssignDB()
task_submit_record_db = TaskSubmitRecordDB()
task_submit_attach_db = TaskSubmitAttachmentDB()
task_submit_tag_db = TaskSubmitTagDB()
task_assign_tag_db = TaskAssignTagDB()
task_assign_attach_db = TaskAssignAttachDB()
task_review_record_db = TaskReviewRecordDB()