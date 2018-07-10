# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=32, blank=True, null=True,verbose_name='部门')

    class Meta:
        db_table = 'department'
        verbose_name = '部门'
        verbose_name_plural = '部门'

    def __str__(self):
        return self.department


class Performemce(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=32,verbose_name='绩效名称')
    personal_score = models.IntegerField(verbose_name='个人分值')
    personal_total = models.IntegerField(verbose_name='个人总分')
    team_score = models.IntegerField(verbose_name='团队分值')
    team_total = models.IntegerField(verbose_name='团队总分')

    class Meta:
        db_table = 'performemce'
        verbose_name = '绩效分类'
        verbose_name_plural = '绩效分类'

    def __str__(self):
        return self.name


class Staff(models.Model):
    sid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64,verbose_name='员工编号')
    department = models.IntegerField(blank=True, null=True,verbose_name='所属部门')

    class Meta:
        db_table = 'staff'
        verbose_name = '员工'
        verbose_name_plural = '员工'

    def __str__(self):
        return self.name


class Task(models.Model):
    execute_way_choice = ((0, '并行执行'), (1, '次序执行'))
    task_status_choice = ((1, '启动'), (2, '暂停'), (3, '终止'))
    is_assign = ((0, '未指派'), (1, '已指派'))
    is_finish = ((0, '未完成'), (1, '已完成'))

    tid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=512,verbose_name='任务名称')  # '任务名称'
    content = models.TextField(verbose_name='任务描述')   # '任务描述',
    # type_id = models.ForeignKey("TaskType",related_name="type_id" ,on_delete=models.CASCADE,db_constraint=False)
    type_id = models.SmallIntegerField(verbose_name='任务类型')  # ' 任务类型',
    issuer_id = models.IntegerField(verbose_name='发布人')  # '发布人',
    perfor_id = models.IntegerField(verbose_name='绩效分类')    # '绩效分类',
    execute_way = models.IntegerField(choices=execute_way_choice, verbose_name='执行方式')   # '0代表并行执行，1次序执行',
    teamwork_auth = models.IntegerField(verbose_name='是否可见')  # '0代表相互可见；1互不可见；2指定可见',
    tcid = models.IntegerField(blank=True, null=True,verbose_name='任务周期')  # 任务周期
    start_time = models.DateTimeField(blank=True, null=True, verbose_name='起始时间')
    deadline = models.DateTimeField(blank=True, null=True, verbose_name='截止时间')
    is_assign = models.IntegerField(choices=is_assign, verbose_name='指派状态')
    is_finish = models.IntegerField(choices=is_finish, verbose_name='完成状态')
    status = models.IntegerField(choices=task_status_choice, verbose_name='任务状态')
    create_time = models.DateTimeField(verbose_name='创建时间')
    last_edit = models.DateTimeField(verbose_name='最后编辑时间')

    class Meta:
        db_table = 'task'
        verbose_name = '工作任务内容'
        verbose_name_plural = '工作任务内容'

    def __str__(self):
        return self.title


class TaskAssign(models.Model):
    tasid = models.AutoField(primary_key=True)
    tid = models.IntegerField(verbose_name='任务编号')
    member_id = models.IntegerField(verbose_name='员工编号')
    title = models.CharField(max_length=512, blank=True, null=True, verbose_name='任务名称')
    content = models.TextField(blank=True, null=True, verbose_name='任务内容')
    deadline = models.DateTimeField(blank=True, null=True, verbose_name='截止时间')
    weight = models.SmallIntegerField(blank=True, null=True)
    is_finish = models.IntegerField(blank=True, null=True,verbose_name='完成状态')
    create_time = models.DateTimeField(verbose_name='创建时间')
    last_edit = models.DateTimeField(verbose_name='最后编辑时间')

    class Meta:
        db_table = 'task_assign'
        unique_together = (('tid', 'member_id'),)
        verbose_name = '任务指派内容'
        verbose_name_plural = '任务指派'

    def __str__(self):
        return "任务指派{0}".format(self.tasid)


class TaskAssignAttach(models.Model):
    taaid = models.AutoField(primary_key=True)
    tasid = models.IntegerField(verbose_name='任务指派编号')
    attachment = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'task_assign_attach'
        verbose_name = '任务指派附件'
        verbose_name_plural = '任务指派附件'

    def __str__(self):
        return "任务指派附件:{0}".format(self.taaid)


class TaskAttachment(models.Model):
    tamid = models.AutoField(primary_key=True)
    tid = models.IntegerField(verbose_name='任务编号')
    attachment = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'task_attachment'
        verbose_name = '任务附件'
        verbose_name_plural = '任务附件'

    def __str__(self):
        return "任务附件:{0}".format(self.name)


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
        verbose_name = '任务审核'
        verbose_name_plural = '任务审核'

    def __str__(self):
        return "任务附件:{0}".format(self.tamid)


class TaskCycle(models.Model):
    tcid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=32, blank=True, null=True, verbose_name='任务周期')

    class Meta:
        db_table = 'task_cycle'
        verbose_name = '任务周期'
        verbose_name_plural = '任务周期'

    def __str__(self):
        return self.name


class TaskReviewRecord(models.Model):
    trrid = models.AutoField(primary_key=True)
    tasid = models.IntegerField(verbose_name='任务指派编号')
    tvid = models.IntegerField(verbose_name='任务审核分配id')
    is_complete = models.SmallIntegerField(verbose_name='审核状态')
    evaluate = models.FloatField(blank=True, null=True, verbose_name='星级评分')
    create_time = models.DateTimeField(verbose_name='审核时间')
    reason = models.TextField(blank=True, null=True, verbose_name='原因')
    comment = models.TextField(blank=True, null=True, verbose_name='评语')

    class Meta:
        db_table = 'task_review_record'
        verbose_name = '任务审核记录'
        verbose_name_plural = '任务审核记录'

    def __str__(self):
        return '任务审核记录{0}'.format(self.trrid)


class TaskReview(models.Model):
    tvid = models.AutoField(primary_key=True)
    tid = models.IntegerField(verbose_name='任务编号')
    sid = models.IntegerField(verbose_name='审核人编号')
    follow = models.IntegerField(verbose_name='审核顺序')

    class Meta:
        db_table = 'task_review'
        unique_together = (('tid', 'sid'),)
        verbose_name = '任务审核人'
        verbose_name_plural = '任务审核人'

    def __str__(self):
        return '任务审核人{0}'.format(self.tvid)


class TaskSubmitAttachment(models.Model):
    tsaid = models.AutoField(primary_key=True)
    tsid = models.IntegerField(verbose_name='任务提交编号')
    attachment = models.CharField(max_length=512, blank=True, null=True,verbose_name='附件路径')
    name = models.CharField(max_length=128, blank=True, null=True,verbose_name='附件名称')
    description = models.CharField(max_length=512, blank=True, null=True,verbose_name='附件描述')

    class Meta:
        db_table = 'task_submit_attachment'
        verbose_name = '任务提交附件'
        verbose_name_plural = '任务提交附件'

    def __str__(self):
        return '任务提交附件{0}'.format(self.tsaid)


class TaskSubmitRecord(models.Model):
    is_assist_choice = ((0, '否'), (1, '是'))
    tsid = models.AutoField(primary_key=True)
    tasid = models.IntegerField(verbose_name='任务指派编号')
    title = models.CharField(max_length=512, blank=True, null=True,verbose_name="标题")
    summary = models.CharField(max_length=512, blank=True, null=True,verbose_name='小结')
    remark = models.CharField(max_length=512, blank=True, null=True,verbose_name='备注')
    completion = models.IntegerField(default=0,verbose_name='完成度(%)')  # 完成度：1-100
    is_assist = models.SmallIntegerField( choices=is_assist_choice, default=0, verbose_name='是否寻求协助')  # 是否寻求协助:0否，1是
    create_time = models.DateTimeField(verbose_name='创建时间')
    last_edit = models.DateTimeField(verbose_name='最后编辑时间')

    class Meta:
        db_table = 'task_submit_record'
        verbose_name = '任务提交记录'
        verbose_name_plural = '任务提交记录'

    def __str__(self):
        return '任务提交记录{0}'.format(self.title)


class TaskTag(models.Model):
    ttid = models.AutoField(primary_key=True)
    tid = models.IntegerField(verbose_name='任务编号')
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='标签名称')

    class Meta:
        db_table = 'task_tag'
        unique_together = (('tid', 'name'),)
        verbose_name = '任务标签'
        verbose_name_plural = '任务标签'

    def __str__(self):
        return '任务提交记录{0}'.format(self.name)


class TaskAssignTag(models.Model):
    tatid = models.AutoField(primary_key=True)
    tasid = models.IntegerField(verbose_name='任务指派编号')
    name = models.CharField(max_length=32, blank=True, null=True,verbose_name='标签名称')

    class Meta:
        db_table = 'task_assign_tag'
        unique_together = (('tasid', 'name'),)
        verbose_name = '指派任务标签'
        verbose_name_plural = '指派任务标签'

    def __str__(self):
        return '任务指派标签{0}'.format(self.name)


class TaskSubmitTag(models.Model):
    tstid = models.AutoField(primary_key=True)
    tsid = models.IntegerField(verbose_name='任务提交编号')
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='标签编号')

    class Meta:
        db_table = 'task_submit_tag'
        unique_together = (('tsid', 'name'),)
        verbose_name = '工作提交标签'
        verbose_name_plural = '工作提交标签'

    def __str__(self):
        return '任务提交标签{0}'.format(self.name)


class TaskType(models.Model):
    tpid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=32, verbose_name='分类名称')

    class Meta:
        db_table = 'task_type'
        verbose_name = '任务类型'
        verbose_name_plural = '任务类型'

    def __str__(self):
        return self.name
