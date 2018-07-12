
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
    name = models.CharField(max_length=64,verbose_name='员工姓名')
    department = models.ForeignKey('Department',to_field="id", on_delete=models.CASCADE, db_constraint=False, default=1, verbose_name='所属部门')

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
    teamwork_auth_choice = ((0, '相互可见'), (1, '互不可见'), (3, '指定可见'))

    tid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=512, verbose_name='任务名称')  # '任务名称'
    content = models.TextField(verbose_name='任务描述')  # '任务描述',
    type = models.ForeignKey("TaskType", to_field="tpid", on_delete=models.CASCADE, verbose_name='任务类型',
                             db_constraint=False, default=1)
    # type_id = models.SmallIntegerField(verbose_name='任务类型')  # ' 任务类型',
    issuer = models.ForeignKey('Staff', to_field="sid", on_delete=models.CASCADE, verbose_name='发布人',
                               db_constraint=False, parent_link=True)  # '发布人',
    perfor = models.ForeignKey('Performemce', to_field='pid', on_delete=models.CASCADE, db_constraint=False,
                               verbose_name='绩效分类')  # '绩效分类',
    execute_way = models.IntegerField(choices=execute_way_choice, verbose_name='执行方式')  # '0代表并行执行，1次序执行',
    teamwork_auth = models.IntegerField(choices=teamwork_auth_choice, default=1,
                                        verbose_name='是否可见')  # '0代表相互可见；1互不可见；2指定可见',
    cycle = models.ForeignKey('TaskCycle', to_field="tcid", on_delete=models.CASCADE, db_constraint=False, default=1,
                              verbose_name='任务周期')  # 任务周期
    # reviewers = models.ManyToManyField("Staff", related_name='task_review',through='TaskReview', verbose_name='审核人',through_fields=('tid','sid'),)
    start_time = models.DateTimeField(blank=True, null=True, verbose_name='起始时间')
    deadline = models.DateTimeField(blank=True, null=True, verbose_name='截止时间')
    is_assign = models.IntegerField(choices=is_assign, verbose_name='指派状态')
    is_finish = models.IntegerField(choices=is_finish, verbose_name='完成状态')
    status = models.IntegerField(choices=task_status_choice, verbose_name='任务状态')
    create_time = models.DateTimeField(verbose_name='创建时间')
    last_edit = models.DateTimeField(verbose_name='最后编辑时间')

    class Meta:
        db_table = 'task'
        verbose_name = '任务内容'
        verbose_name_plural = '任务内容'

    def __str__(self):
        return self.title


class TaskAssign(models.Model):
    is_finish = ((0, '未完成'), (1, '已完成'))
    tasid = models.AutoField(primary_key=True)
    tid = models.ForeignKey('Task', to_field='tid', on_delete=models.CASCADE, db_constraint=False, verbose_name='任务')
    member_id = models.ForeignKey('Staff', to_field="sid", on_delete=models.CASCADE, verbose_name='员工',
                                  db_constraint=False)
    title = models.CharField(max_length=512, blank=True, null=True, verbose_name='任务名称')
    content = models.TextField(blank=True, null=True, verbose_name='任务内容')
    deadline = models.DateTimeField(blank=True, null=True, verbose_name='截止时间')
    weight = models.SmallIntegerField(blank=True, null=True)
    is_finish = models.IntegerField(choices=is_finish, default=0, verbose_name='完成状态')
    create_time = models.DateTimeField(verbose_name='创建时间')
    last_edit = models.DateTimeField(verbose_name='最后编辑时间')

    class Meta:
        db_table = 'task_assign'
        unique_together = (('tid', 'member_id'),)
        verbose_name = '任务指派内容'
        verbose_name_plural = '任务指派'

    def __str__(self):
        return "任务指派:{0}".format(self.tid)


class TaskAssignAttach(models.Model):
    taaid = models.AutoField(primary_key=True)
    tasid = models.ForeignKey('TaskAssign', to_field='tasid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='指派任务')
    attachment = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'task_assign_attach'
        verbose_name = '任务指派附件'
        verbose_name_plural = '任务指派附件'

    def __str__(self):
        return "任务指派附件:{0}".format(self.tasid)


class TaskAttachment(models.Model):
    tamid = models.AutoField(primary_key=True)
    tid = models.ForeignKey('Task', to_field='tid', on_delete=models.CASCADE, db_constraint=False, verbose_name='任务')
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
    tasid = models.ForeignKey('TaskAssign', to_field='tasid', on_delete=models.CASCADE, db_constraint=False,verbose_name='指派任务')
    status = models.IntegerField()
    result = models.IntegerField()
    score = models.IntegerField()
    create_time = models.DateTimeField()
    last_edit = models.DateTimeField()

    class Meta:
        db_table = 'task_auth'
        verbose_name = ''
        verbose_name_plural = ''

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
    is_complete = ((0, '未完成'), (1, '已完成'))
    trrid = models.AutoField(primary_key=True)
    tasid = models.ForeignKey('TaskAssign', to_field='tasid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='指派任务')
    tvid = models.ForeignKey('TaskReview', to_field='tvid', on_delete=models.CASCADE, db_constraint=False,
                             verbose_name='任务审核分配id')
    is_complete = models.SmallIntegerField(choices=is_complete, verbose_name='审核状态')
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
    tid = models.ForeignKey('Task', to_field='tid', on_delete=models.CASCADE, db_constraint=False, verbose_name='任务')
    sid = models.ForeignKey("Staff", to_field='sid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='审核人')
    follow = models.IntegerField(verbose_name='审核顺序')

    class Meta:
        db_table = 'task_review'
        unique_together = (('tid', 'sid'),)
        verbose_name = '任务审核人'
        verbose_name_plural = '任务审核人'

    def __str__(self):
        return '任务审核人{0}'.format(self.sid)


class TaskSubmitAttachment(models.Model):
    tsaid = models.AutoField(primary_key=True)
    tsid = models.ForeignKey('TaskSubmitRecord', to_field='tsid', on_delete=models.CASCADE, db_constraint=False,
                             verbose_name='工作提交')
    attachment = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'task_submit_attachment'
        verbose_name = '工作提交附件'
        verbose_name_plural = '工作提交附件'

    def __str__(self):
        return '工作提交附件{0}'.format(self.tsaid)


class TaskSubmitRecord(models.Model):
    is_assist_choice = ((0, '否'), (1, '是'))

    tsid = models.AutoField(primary_key=True)
    tasid = models.ForeignKey('TaskAssign', to_field='tasid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='指派任务')
    title = models.CharField(max_length=512, blank=True, null=True, verbose_name="标题")
    summary = models.CharField(max_length=512, blank=True, null=True, verbose_name='小结')
    remark = models.CharField(max_length=512, blank=True, null=True, verbose_name='备注')
    completion = models.IntegerField(default=0, verbose_name='完成度(%)')  # 完成度：1-100
    is_assist = models.SmallIntegerField(choices=is_assist_choice, default=0, verbose_name='是否寻求协助')  # 是否寻求协助:0否，1是
    create_time = models.DateTimeField(verbose_name='创建时间')
    last_edit = models.DateTimeField(verbose_name='最后编辑时间')

    class Meta:
        db_table = 'task_submit_record'
        verbose_name = '工作提交记录'
        verbose_name_plural = '工作提交记录'

    def __str__(self):
        return '工作提交记录{0}'.format(self.title)


class TaskTag(models.Model):
    ttid = models.AutoField(primary_key=True)
    tid = models.ForeignKey('Task', to_field='tid', on_delete=models.CASCADE, db_constraint=False, verbose_name='任务')
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
    tasid = models.ForeignKey('TaskAssign', to_field='tasid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='指派任务')
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='标签名称')

    class Meta:
        db_table = 'task_assign_tag'
        unique_together = (('tasid', 'name'),)
        verbose_name = '任务指派标签'
        verbose_name_plural = '任务指派标签'

    def __str__(self):
        return '任务指派标签{0}'.format(self.tasid)


class TaskSubmitTag(models.Model):
    tstid = models.AutoField(primary_key=True)
    tsid = models.ForeignKey('TaskSubmitRecord', to_field='tsid', on_delete=models.CASCADE, db_constraint=False,
                             verbose_name='任务提交')
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='标签')

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
