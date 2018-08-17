from django.db import connection
from datetime import timedelta
from .models import *




class PerformanceDB(object):
    """绩效表"""
    def query_performence_list(self):
        result_db = Performance.objects.filter().all().order_by("-pid")
        return result_db

    def query_performence_by_pid(self, pid):
        result_db = Performance.objects.filter(pid=pid).first()
        return result_db

    def insert_performence(self, modify_info):
        is_exists = Performance.objects.filter(name=modify_info['name'])
        if is_exists:
            raise Exception('绩效已存在')
        Performance.objects.create(**modify_info)

    def update_performence(self, modify_info):
        Performance.objects.filter(pid=modify_info['pid']).update(**modify_info)

    def mutil_delete_performence(self, id_list):
        Performance.objects.filter(pid__in=id_list).delete()


class PerformanceRecordDB(object):

    def insert_performence_record(self, modify_info):
        is_exists = PerformanceRecord.objects.filter(tmid=modify_info['tmid'], sid=modify_info['sid'])
        if not is_exists:
            PerformanceRecord.objects.create(**modify_info)

    def update_performence_record(self, modify_info):
        query_set = PerformanceRecord.objects.filter(tmid=modify_info["tmid"], sid=modify_info['sid']).first()
        if query_set:
            query_set.team_score = modify_info['team_score']
            query_set.save()
        else:
            self.insert_performence_record(**modify_info)

    def query_total_score(self,condition):
        sql = """select prid,tmid_id, sid_id,sum(personal_score) as p_score,sum(team_score) as t_score from performance_record 
               left join staff  on sid_id=staff.sid
               left join department on staff.department_id = department.id {0} GROUP BY sid_id"""
        query ="where performance_record.create_time Between '{0}' AND '{1}' ".format(condition['first_day'],condition['last_day'])
        filter = ''
        if condition.get("sid",None):
            filter += " staff.sid={0}".format(condition["sid"])
        elif condition.get("dpid",None):
            filter += " department.id={0}".format(condition["dpid"])
        if filter:
            query += " AND "
            query += filter
        sql=sql.format(query)
        result_db = PerformanceRecord.objects.raw(sql)
        return result_db

    def query_perfor_score_by_sid(self,sid, first_day, last_day):
        result_db=PerformanceRecord.objects.filter(sid_id=sid,create_time__range=(first_day,last_day+timedelta(days=1))).all()
        return result_db


class TaskDB(object):
    """任务表列表"""
    # 任务状态
    task_status = (
        {"id": 0, "caption": "删除"},
        {"id": 1, "caption": "启动"},
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
        result_db = Task.objects.filter(delete_status__gt=0).all().order_by("-tid")
        return result_db

    def query_task_by_tid(self, tid):
        result_db = Task.objects.filter(tid=tid,).first()
        return result_db

    def query_task_by_tids(self,tids):
        result_db = Task.objects.filter(tid__in=tids,).all()
        return result_db

    def query_task_by_type(self, type_id):
        result_db = Task.objects.filter(type_id=type_id,).all()
        return result_db

    def query_task_by_issuer_id(self, issuer_id):
        result_db = Task.objects.filter(issuer_id=issuer_id).first()
        return result_db

    def multi_delete_task(self, id_list, delete_status):
        Task.objects.filter(tid__in=id_list).update(**delete_status)

    def update_task_status_by_tid(self, tid,modify_info):
        Task.objects.filter(tid=tid).update(**modify_info)


class TaskMapDB(object):
    """任务表列表"""
    # 任务状态
    task_status = (
        {"id": 1, "caption": "进行中"},
        {"id": 2, "caption": "已完成"},
        {"id": 3, "caption": "已暂停"},
        {"id": 4, "caption": "已终止"},
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
        {"id": 0, "caption": "进行中"},
        {"id": 1, "caption": "已完成"}
    )
    # 任务方式
    task_way = (
        {"id": 0, "caption": "个人任务"},
        {"id": 1, "caption": "组队任务"}
    )

    def insert_task(self, modify_info):
        task_sql = """insert into task_map(%s) value(%s);"""
        k_list = []
        v_list = []
        for k, v in modify_info.items():
            k_list.append(k)
            v_list.append("%%(%s)s" % k)
        task_sql = task_sql % (",".join(k_list), ",".join(v_list))
        cursor = connection.cursor()
        cursor.execute(task_sql, modify_info)
        tmid = cursor.lastrowid
        return tmid

    def update_task(self, modify_info):
        result_db=TaskMap.objects.filter(tmid=modify_info['tmid']).update(**modify_info)
        return result_db

    def query_task_lists(self):
        result_db = TaskMap.objects.filter().all().order_by("-tmid")
        return result_db

    def query_task_by_is_assign(self,):
        result_db = TaskMap.objects.all()
        return result_db

    def query_task_assign_lists(self):
        result_db = TaskMap.objects.all().order_by("-tmid")
        return result_db

    def query_task_by_tid(self, tid):
        result_db = TaskMap.objects.filter(tid_id=tid).all()
        return result_db

    def query_task_by_tmid(self, tmid):
        result_db = TaskMap.objects.filter(tmid=tmid).first()
        return result_db

    def query_task_by_tids(self,tmids):
        result_db = TaskMap.objects.filter(tmid__in=tmids).all()
        return result_db

    def query_task_by_assigner_id(self, assigner):
        result_db = TaskMap.objects.filter(assigner=assigner).first()
        return result_db

    def multi_delete_task(self, id_list):
        TaskMap.objects.filter(tmid__in=id_list).delete()

    def update_task_status_by_tid(self, tmid,modify_info):
        TaskMap.objects.filter(tmid=tmid).update(**modify_info)


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
        is_exist = TaskType.objects.filter(name=modify_info['name']).first()
        if is_exist:
            raise Exception("该分类名称已存在")
        TaskType.objects.create(**modify_info)

    def query_task_type_by_id(self, tpid):
        result_db = TaskType.objects.filter(tpid=tpid).first()
        return result_db

    def update_task_type(self, modify_info):
        is_exist = TaskType.objects.filter(name=modify_info['name']).first()
        if is_exist:
            raise Exception("该分类名称已存在")
        TaskType.objects.filter(tpid=modify_info["tpid"]).update(**modify_info)

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

    def query_task_reviewer_by_tmid(self,tmid):
        result_db = TaskReview.objects.filter(tmid_id=tmid).all()
        return result_db

    def query_task_reviewer_by_sid(self,sid):
        result_db = TaskReview.objects.filter(sid_id=sid).all()
        return result_db

    def query_task_reviewer_by_tvid(self,tvid):
        result_db = TaskReview.objects.filter(tvid=tvid).first()
        return result_db

    def query_task_reviewer_by_tid_sid(self, tmid, sid):
        result_db = TaskReview.objects.filter(tmid_id=tmid, sid_id=sid).first()
        return result_db

    def query_task_reviewer_by_tid_follow(self, tmid, pre_follow):
        result_db =TaskReview.objects.filter(tmid_id=tmid,follow=pre_follow).first()
        return result_db

    def mutil_update_reviewer(self, modify_info):
        for item in modify_info:
            TaskReview.objects.filter(tmid_id=item['tmid_id'], sid_id=item['sid_id']).update(**item)

    def mutil_delete_reviewer(self, id_list):
        TaskReview.objects.filter(tvid__in=id_list).delete()

    def mutil_delete_reviewer_by_tid(self,tid_list):
        TaskReview.objects.filter(tmid_id__in=tid_list).delete()


class TaskAssignDB(object):
    """任务指派表"""
    # 是否完成
    is_finish = (
        {"id": 0, "caption": "进行中"},
        {"id": 1, "caption": "已完成"}
    )

    def mutil_insert_task_assign(self, modify_info_list):
        for item in modify_info_list:
            is_exist = TaskAssign.objects.filter(tmid_id=item['tmid_id'], member_id_id=item['member_id_id'])
            if is_exist:
                continue
            TaskAssign.objects.create(**item)

    def update_task_assign(self, modify_info):
        TaskAssign.objects.filter(tasid=modify_info["tasid"]).update(**modify_info)

    # def update_progress(self,tasid, progress):
    #     TaskAssign.objects.filter(tasid=tasid).update(progress=progress)

    def query_task_assign_by_tmid(self, tmid):
        result_db = TaskAssign.objects.filter(tmid_id=tmid).all()
        return result_db

    def query_task_assign_by_tasid(self, tasid):
        result_db = TaskAssign.objects.filter(tasid=tasid)
        return result_db

    def query_task_assign_by_member_id(self, member_id):
        result_db = TaskAssign.objects.filter(member_id=member_id).all()
        return result_db

    def mutil_delete_assign_by_tasid(self,id_list):
        TaskAssign.objects.filter(tasid__in=id_list).delete()

    def count_personal_total_task(self, sid, first_day, last_day):
        result_db = TaskAssign.objects.filter(member_id_id=sid,tmid_id__team=0,deadline__range=(first_day,last_day+timedelta(days=1))).count()
        return result_db

    def count_personal_finish_task(self, sid, first_day, last_day):
        result_db = TaskAssign.objects.filter(member_id_id=sid,is_finish=1,tmid_id__team=0, deadline__range=(first_day, last_day+timedelta(days=1))).count()
        return result_db

    def count_team_total_task(self, sid, first_day, last_day):
        result_db = TaskAssign.objects.filter(member_id_id=sid, tmid_id__team=1, deadline__range=(first_day,last_day+timedelta(days=1))).count()
        return result_db

    def count_team_finish_task(self, sid, first_day, last_day):
        result_db = TaskAssign.objects.filter(member_id_id=sid,is_finish=1,tmid_id__team=1,deadline__range=(first_day, last_day+timedelta(days=1))).count()
        return result_db


class TaskSubmitRecordDB(object):
    """任务提交记录表"""

    def query_last_submit_record(self, tasid):
        result_db = TaskSubmitRecord.objects.filter(tasid_id=tasid).last()
        return result_db

    def query_submit_by_tasid(self, tasid):
        result_db = TaskSubmitRecord.objects.filter(tasid_id=tasid).all().order_by("-tsid")
        return result_db

    def query_submit_by_tasid_list(self,tasid_list):
        resutl_db = TaskSubmitRecord.objects.filter(tasid__in=tasid_list).order_by('-tsid').all()[0:10]
        return resutl_db

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
            is_exists = TaskSubmitTag.objects.filter(tsid_id=item['tsid_id'], name=item['name'])
            if is_exists:
                continue
            TaskSubmitTag.objects.create(**item)

    def mutil_update_tag(self, modify_info_list):
        for item in modify_info_list:
            TaskSubmitTag.objects.filter(tstid=item['tstid']).update(**item)

    def mutil_delete_tag(self, id_list):
        TaskSubmitTag.objects.filter(tstid__in=id_list).delete()

    def mutil_delete_tag_by_tsid(self, id_list):
        TaskSubmitTag.objects.filter(tsid_id__in=id_list).delete()

    def query_task_tag_by_tsid(self, tsid):
        result_db = TaskSubmitTag.objects.filter(tsid_id=tsid).all()
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

    def mutil_delete_tag_by_tasid(self,tasid_list):
        TaskAssignTag.objects.filter(tasid__in=tasid_list).delete()


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

    def mutil_delete_attach_by_tasid(self, id_list):
        TaskAssignAttach.objects.filter(tasid__in=id_list).delete()


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


task_db = TaskDB()
task_map_db = TaskMapDB()
task_cycle_db = TaskCycleDB()
task_type_db = TaskTypeDB()
task_attachment_db = TaskAttachmentDB()
task_tag_db = TaskTagDB()
task_review_db = TaskReviewDB()
performence_db = PerformanceDB()
performance_record_db = PerformanceRecordDB()
task_assign_db = TaskAssignDB()
task_submit_record_db = TaskSubmitRecordDB()
task_submit_attach_db = TaskSubmitAttachmentDB()
task_submit_tag_db = TaskSubmitTagDB()
task_assign_tag_db = TaskAssignTagDB()
task_assign_attach_db = TaskAssignAttachDB()
task_review_record_db = TaskReviewRecordDB()