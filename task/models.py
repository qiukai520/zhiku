# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Department(models.Model):
    department = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'department'


class Performemce(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=32)
    personal_score = models.IntegerField()
    personal_total = models.IntegerField()
    team_score = models.IntegerField()
    team_total = models.IntegerField()

    class Meta:
        db_table = 'performemce'


class Staff(models.Model):
    sid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    department = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'staff'


class Task(models.Model):
    tid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=512)  # '任务名称'
    content = models.TextField()   # '任务描述',
    type_id = models.SmallIntegerField()  # ' 任务类型',
    issuer_id = models.IntegerField()  # '发布人',
    perfor_id = models.IntegerField()    # '绩效分类',
    execute_way = models.IntegerField()   # '0代表并行执行，1次序执行',
    teamwork_auth = models.IntegerField()
    tcid = models.IntegerField(blank=True, null=True) #任务周期
    start_time = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    is_assign = models.IntegerField()
    is_finish = models.IntegerField()
    status = models.IntegerField()
    create_time = models.DateTimeField()
    last_edit = models.DateTimeField()

    class Meta:
        db_table = 'task'


class TaskAssign(models.Model):
    tasid = models.AutoField(primary_key=True)
    tid = models.IntegerField()
    member_id = models.IntegerField()
    title = models.CharField(max_length=512, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    weight = models.SmallIntegerField(blank=True, null=True)
    is_finish = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField()
    last_edit = models.DateTimeField()

    class Meta:
        db_table = 'task_assign'
        unique_together = (('tid', 'member_id'),)


class TaskAssignAttach(models.Model):
    taaid = models.AutoField(primary_key=True)
    tasid = models.IntegerField()
    attachment = models.CharField(max_length=512, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'task_assign_attach'


class TaskAttachment(models.Model):
    tamid = models.AutoField(primary_key=True)
    tid = models.IntegerField()
    attachment = models.CharField(max_length=512, blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'task_attachment'


class TaskAuth(models.Model):
    taid = models.AutoField(primary_key=True)
    tasid = models.IntegerField()
    status = models.IntegerField()
    result = models.IntegerField()
    score = models.IntegerField()
    create_time = models.DateTimeField()
    last_edit = models.DateTimeField()

    class Meta:
        db_table = 'task_auth'


class TaskCycle(models.Model):
    tcid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'task_cycle'


class TaskRejectRecord(models.Model):
    trid = models.AutoField(primary_key=True)
    tasid = models.IntegerField()
    create_time = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'task_reject_record'


class TaskReview(models.Model):
    tvid = models.AutoField(primary_key=True)
    tid = models.IntegerField()
    sid = models.IntegerField()
    follow = models.IntegerField()

    class Meta:
        db_table = 'task_review'
        unique_together = (('tid', 'sid'),)


class TaskSubmitAttachment(models.Model):
    tsaid = models.AutoField(primary_key=True)
    tsid = models.IntegerField()
    attachment = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'task_submit_attachment'


class TaskSubmitRecord(models.Model):
    tsid = models.AutoField(primary_key=True)
    tasid = models.IntegerField()
    title = models.CharField(max_length=512, blank=True, null=True)
    summary = models.CharField(max_length=512, blank=True, null=True)
    remark = models.CharField(max_length=512, blank=True, null=True)
    completion = models.IntegerField(default=0)  # 完成度：1-100
    create_time = models.DateTimeField()
    last_edit = models.DateTimeField()

    class Meta:
        db_table = 'task_submit_record'


class TaskTag(models.Model):
    ttid = models.AutoField(primary_key=True)
    tid = models.IntegerField()
    name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'task_tag'
        unique_together = (('tid', 'name'),)


class TaskAssignTag(models.Model):
    tatid = models.AutoField(primary_key=True)
    tasid = models.IntegerField()
    name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'task_assign_tag'
        unique_together = (('tasid', 'name'),)

class TaskSubmitTag(models.Model):
    tstid = models.AutoField(primary_key=True)
    tsid = models.IntegerField()
    name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'task_submit_tag'
        unique_together = (('tsid', 'name'),)

class TaskType(models.Model):
    tpid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=32)

    class Meta:
        db_table = 'task_type'
