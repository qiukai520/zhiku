
from django.db import models
from personnel.models import Staff


class Performance(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=32, verbose_name='绩效名称')
    personal_score = models.IntegerField(verbose_name='个人分值')
    personal_total = models.IntegerField(verbose_name='个人总分')
    team_score = models.IntegerField(verbose_name='团队分值')
    team_total = models.IntegerField(verbose_name='团队总分')

    class Meta:
        db_table = 'performance'
        verbose_name = '绩效分类'
        verbose_name_plural = '绩效分类'

    def __str__(self):
        return self.name

    _insert = ['name', "personal_score", "team_socre","personal_total","team_score"]
    _update = ['name', "personal_score", "team_socre","personal_total","team_score"]


# 绩效记录
class PerformanceRecord(models.Model):
    prid = models.AutoField(primary_key=True)
    sid = models.ForeignKey(Staff, to_field='sid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='员工')
    tmid = models.ForeignKey('TaskMap', to_field='tmid', on_delete=models.CASCADE, db_constraint=False, verbose_name='任务')
    personal_score = models.IntegerField(verbose_name="个人分值", default=0)
    team_score = models.IntegerField(verbose_name="团队分值", default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'performance_record'
        verbose_name = '任务绩效记录'
        verbose_name_plural = '任务绩效记录'


class Task(models.Model):
    task_status_choice = ((1, '启动'), (0, '删除'))

    tid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=512, verbose_name='任务名称')  # 任务名称
    content = models.TextField(verbose_name='任务描述')  # 任务描述',
    type = models.ForeignKey("TaskType", to_field="tpid", on_delete=models.CASCADE, verbose_name='任务类型',
                             db_constraint=False, default=1)
    issuer = models.ForeignKey(Staff, to_field="sid", on_delete=models.CASCADE, verbose_name='发布人',
                               db_constraint=False, parent_link=True)  # '发布人',
    delete_status = models.IntegerField(choices=task_status_choice, default=1, verbose_name='删除状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'task'
        verbose_name = '任务内容'
        verbose_name_plural = '任务内容'

    def __str__(self):
        return self.title


class TaskMap(models.Model):
    execute_way_choice = ((0, '并行执行'), (1, '次序执行'))
    task_status_choice = ((0, '已删除'), (1, '进行中'), (2, '已暂停'), (3, '已取消'), )
    is_finish = ((0, '进行中'), (1, '已完成'))
    teamwork_auth_choice = ((0, '相互可见'), (1, '互不可见'), (3, '指定可见'))
    team_choice = ((0, '个人任务'), (1, '组队任务'))
    cycle_choice = ((1, "单次"), (2, "每天"), (3, "每周"), (4, "每月"))

    tmid = models.AutoField(primary_key=True)
    tid = models.ForeignKey("Task", to_field="tid", on_delete=models.CASCADE, verbose_name='任务',
                            db_constraint=False)
    title = models.CharField(max_length=512, verbose_name='任务名称')  # 任务名称
    content = models.TextField(verbose_name='任务描述')  # 任务描述',
    type = models.ForeignKey("TaskType", to_field="tpid", on_delete=models.CASCADE, verbose_name='任务类型',
                             db_constraint=False, default=1)
    assigner = models.ForeignKey(Staff, to_field="sid", on_delete=models.CASCADE, verbose_name='指派人',
                                 db_constraint =False, parent_link=True)  # '指派人',
    perfor = models.ForeignKey('Performance', to_field='pid', on_delete=models.CASCADE, db_constraint=False,
                               verbose_name='绩效分类')  # '绩效分类',
    execute_way = models.IntegerField(choices=execute_way_choice, verbose_name='执行方式')  # '0代表并行执行，1次序执行',
    teamwork_auth = models.IntegerField(choices=teamwork_auth_choice, default=1,
                                        verbose_name='是否可见')  # '0代表相互可见；1互不可见；2指定可见',
    # cycle = models.ForeignKey('TaskCycle', to_field="tcid", on_delete=models.CASCADE, db_constraint=False, default=1,
    #                           verbose_name='任务周期')  # 任务周期
    cycle_id = models.SmallIntegerField(choices=cycle_choice, verbose_name='任务周期')
    start_time = models.DateTimeField(blank=True, null=True, verbose_name='起始时间')
    deadline = models.DateTimeField(blank=True, null=True, verbose_name='截止时间')
    is_finish = models.IntegerField(choices=is_finish, default=0, verbose_name='完成状态')
    team = models.IntegerField(choices=team_choice, default=0, verbose_name='任务方式')
    remark = models.CharField(max_length=512, blank=True, null=True, verbose_name='备注')
    status = models.IntegerField(choices=task_status_choice, default=1, verbose_name='任务状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'task_map'
        verbose_name = '任务指派记录'
        verbose_name_plural = '任务指派记录'

    def __str__(self):
        return "任务:{0}".format(self.tid)

    _insert = ["tid_id","title","content","type_id","assigner_id","perfor_id","execute_way","teamwork_auth","cycle_id",
               "start_time","deadline","team","remark","status"]


class TaskPeriod(models.Model):
    execute_way_choice = ((0, '并行执行'), (1, '次序执行'))
    task_status_choice = ((0, '已删除'), (1, '进行中'), (2, '已暂停'), (3, '已取消'), )
    is_finish = ((0, '进行中'), (1, '已完成'))
    teamwork_auth_choice = ((0, '相互可见'), (1, '互不可见'), (3, '指定可见'))
    team_choice = ((0, '个人任务'), (1, '组队任务'))
    cycle_choice = ((1, "单次"), (2, "每天"), (3, "每周"), (4, "每月"))

    tpid = models.AutoField(primary_key=True)
    tid = models.ForeignKey("Task", to_field="tid", on_delete=models.CASCADE, verbose_name='任务',
                            db_constraint=False)
    title = models.CharField(max_length=512, verbose_name='任务名称')  # 任务名称
    content = models.TextField(verbose_name='任务描述')  # 任务描述',
    type = models.ForeignKey("TaskType", to_field="tpid", on_delete=models.CASCADE, verbose_name='任务类型',
                             db_constraint=False, default=1)
    assigner = models.ForeignKey(Staff, to_field="sid", on_delete=models.CASCADE, verbose_name='指派人',
                                 db_constraint =False, parent_link=True)  # '指派人',
    perfor = models.ForeignKey('Performance', to_field='pid', on_delete=models.CASCADE, db_constraint=False,
                               verbose_name='绩效分类')  # '绩效分类',
    execute_way = models.IntegerField(choices=execute_way_choice, verbose_name='执行方式')  # '0代表并行执行，1次序执行',
    teamwork_auth = models.IntegerField(choices=teamwork_auth_choice, default=1,
                                        verbose_name='是否可见')  # '0代表相互可见；1互不可见；2指定可见',
    # cycle = models.ForeignKey('TaskCycle', to_field="tcid", on_delete=models.CASCADE, db_constraint=False, default=1,
    #                           verbose_name='任务周期')  # 任务周期
    cycle_id = models.SmallIntegerField(choices=cycle_choice, verbose_name='任务周期')
    start_time = models.DateTimeField(blank=True, null=True, verbose_name='起始时间')
    deadline = models.DateTimeField(blank=True, null=True, verbose_name='截止时间')
    is_finish = models.IntegerField(choices=is_finish, default=0, verbose_name='完成状态')
    team = models.IntegerField(choices=team_choice, default=0, verbose_name='任务方式')
    remark = models.CharField(max_length=512, blank=True, null=True, verbose_name='备注')
    status = models.IntegerField(choices=task_status_choice, default=1, verbose_name='任务状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'task_period'
        verbose_name = '周期任务'
        verbose_name_plural = '周期任务'

    def __str__(self):
        return "周期任务:{0}".format(self.tid)





class TaskPeriodAttachment(models.Model):
    tpaid = models.AutoField(primary_key=True)
    tpid = models.ForeignKey('TaskPeriod', to_field='tpid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='周期任务内容')
    attachment = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'task_period_attachment'
        verbose_name = '周期附件'
        verbose_name_plural = '周期任务附件'

    def __str__(self):
        return "周期任务附件:{0}".format(self.name)


class TaskPeriodTag(models.Model):
    tptid = models.AutoField(primary_key=True)
    tpid = models.ForeignKey('TaskPeriod', to_field='tpid', on_delete=models.CASCADE, db_constraint=False, verbose_name= '周期任务')
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='标签名称')

    class Meta:
        db_table = 'task_period_tag'
        unique_together = (('tpid', 'name'),)
        verbose_name = '周期任务标签'
        verbose_name_plural = '周期任务标签'

    def __str__(self):
        return '周期任务标签:{0}'.format(self.name)


class TaskPeriodReview(models.Model):
    delete_status_choice = ((0, '已删除'), (1, '保留'))
    tvid = models.AutoField(primary_key=True)
    tpid = models.ForeignKey('TaskPeriod', to_field='tpid', on_delete=models.CASCADE, db_constraint=False, verbose_name='任务')
    sid = models.ForeignKey(Staff, to_field='sid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='审核人')
    follow = models.IntegerField(verbose_name='审核顺序')
    delete_status = models.SmallIntegerField(choices=delete_status_choice,default=1, verbose_name='删除状态')

    class Meta:
        db_table = 'task_period_review'
        unique_together = (('tpid', 'sid'),)
        verbose_name = '周期任务审核人'
        verbose_name_plural = '周期任务审核人'

    def __str__(self):
        return '周期任务审核人{0}'.format(self.sid)


class TaskPeriodAssigner(models.Model):
    tpaid = models.AutoField(primary_key=True)
    tpid = models.ForeignKey('TaskPeriod', to_field='tpid', on_delete=models.CASCADE, db_constraint=False, verbose_name='任务')
    member_id = models.ForeignKey(Staff, to_field='sid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='审核人')

    class Meta:
        db_table = 'task_period_assigner'
        unique_together = (('tpid', 'member_id'),)
        verbose_name = '周期任务指派人'
        verbose_name_plural = '周期任务指派人'

    def __str__(self):
        return '周期任务指派人{0}'.format(self.sid)


class TaskAssign(models.Model):
    is_finish = ((0, '进行中'), (1, '已完成'))
    delete_status_choice = ((0, '已删除'), (1, '保留'))
    status_choice = ((0, '已取消'), (1, "进行中"), (2,"已暂停"))
    tasid = models.AutoField(primary_key=True)
    tmid = models.ForeignKey('TaskMap', to_field='tmid', on_delete=models.CASCADE, db_constraint=False, verbose_name='任务')
    member_id = models.ForeignKey(Staff, to_field="sid", on_delete=models.CASCADE, verbose_name='员工',
                                  db_constraint=False)
    title = models.CharField(max_length=512, blank=True, null=True, verbose_name='任务名称')
    content = models.TextField(blank=True, null=True, verbose_name='任务内容')
    start_time = models.DateTimeField(blank=True, null=True, verbose_name='开始时间')
    deadline = models.DateTimeField(blank=True, null=True, verbose_name='截止时间')
    progress = models.SmallIntegerField(default=0, verbose_name='完成进度(%)')
    is_finish = models.SmallIntegerField(choices=is_finish, default=0, verbose_name='审核状态')
    status = models.SmallIntegerField(choices=status_choice, default=1, verbose_name='任务状态')
    delete_status = models.SmallIntegerField(choices=delete_status_choice, default=1, verbose_name='删除状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')
    class Meta:
        db_table = 'task_assign'
        unique_together = (('tmid', 'member_id'),)
        verbose_name = '个人指派内容'
        verbose_name_plural = '个人指派内容'

    def __str__(self):
        return "个人指派内容:{0}".format(self.title)


class TaskAssignAttach(models.Model):
    taaid = models.AutoField(primary_key=True)
    tasid = models.ForeignKey('TaskAssign', to_field='tasid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='个人指派任务')
    attachment = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'task_assign_attach'
        verbose_name = '个人指派附件'
        verbose_name_plural = '个人指派附件'

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


class TaskMapAttachment(models.Model):
    tmaid = models.AutoField(primary_key=True)
    tmid = models.ForeignKey('TaskMap', to_field='tmid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name ='任务指派内容')
    attachment = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'task_map_attachment'
        verbose_name = '任务指派附件'
        verbose_name_plural = '任务指派附件'

    def __str__(self):
        return "任务指派附件:{0}".format(self.name)


class TaskAuth(models.Model):
    taid = models.AutoField(primary_key=True)
    tasid = models.ForeignKey('TaskAssign', to_field='tasid', on_delete=models.CASCADE, db_constraint=False,verbose_name='指派任务')
    status = models.IntegerField()
    result = models.IntegerField()
    score = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间',)
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'task_auth'
        verbose_name = ''
        verbose_name_plural = ''

    def __str__(self):
        return "任务附件:{0}".format(self.tasid)


class TaskCycle(models.Model):
    tcid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=32, blank=True, null=True, verbose_name='任务周期')
    number = models.SmallIntegerField(verbose_name="周期编号")

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
    reason = models.TextField(blank=True, null=True, verbose_name='原因')
    comment = models.TextField(blank=True, null=True, verbose_name='评语')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='审核时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
            db_table = 'task_review_record'
            verbose_name = '任务审核记录'
            verbose_name_plural = '任务审核记录'

    def __str__(self):
        return '任务审核记录{0}'.format(self.trrid)



class TaskReviewResult(models.Model):
    result_choice = ((0, '未审核'),(1,'未通过'), (2, "通过"), (1, '自动通过'))
    trrid = models.AutoField(primary_key=True)
    tasid = models.ForeignKey('TaskAssign', to_field='tasid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='指派任务')
    sid = models.ForeignKey(Staff, to_field='sid', on_delete=models.CASCADE, db_constraint=False,
                             verbose_name='审核人')
    follow = models.SmallIntegerField(verbose_name='审核顺序')
    result = models.SmallIntegerField(choices=result_choice, verbose_name='审核状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='审核时间')

    class Meta:
            db_table = 'task_review_result'
            verbose_name = '任务审核结果'
            verbose_name_plural = '任务审核结果'

    def __str__(self):
        return '任务审核结果{0}'.format(self.trrid)


class TaskReview(models.Model):
    delete_status_choice = ((0, '已删除'), (1, '保留'))
    tvid = models.AutoField(primary_key=True)
    tmid = models.ForeignKey('TaskMap', to_field='tmid', on_delete=models.CASCADE, db_constraint=False, verbose_name='任务')
    sid = models.ForeignKey(Staff, to_field='sid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='审核人')
    follow = models.IntegerField(verbose_name='审核顺序')
    delete_status = models.SmallIntegerField(choices=delete_status_choice,default=1, verbose_name='删除状态')

    class Meta:
        db_table = 'task_review'
        unique_together = (('tmid', 'sid'),)
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
    completion = models.SmallIntegerField(default=0, verbose_name='完成度(%)')  # 完成度：1-100
    is_assist = models.SmallIntegerField(choices=is_assist_choice, default=0, verbose_name='是否寻求协助')  # 是否寻求协助:0否，1是
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

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
        return '任务标签：{0}'.format(self.name)


class TaskMapTag(models.Model):
    tmtid = models.AutoField(primary_key=True)
    tmid = models.ForeignKey('TaskMap', to_field='tmid', on_delete=models.CASCADE, db_constraint=False, verbose_name='任务指派')
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='标签名称')

    class Meta:
        db_table = 'task_map_tag'
        unique_together = (('tmid', 'name'),)
        verbose_name = '任务指派标签'
        verbose_name_plural = '任务指派标签'

    def __str__(self):
        return '任务指派标签:{0}'.format(self.name)


class TaskAssignTag(models.Model):
    tatid = models.AutoField(primary_key=True)
    tasid = models.ForeignKey('TaskAssign', to_field='tasid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='指派任务')
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='标签名称')

    class Meta:
        db_table = 'task_assign_tag'
        unique_together = (('tasid', 'name'),)
        verbose_name = '个人指派标签'
        verbose_name_plural = '个人指派标签'

    def __str__(self):
        return '个人指派标签{0}'.format(self.tasid)


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

    _insert = ["name"]
    _update = ["name"]
