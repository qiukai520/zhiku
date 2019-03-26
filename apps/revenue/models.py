from django.db import models
from personnel.models import Staff, Company, Project

# Create your models here.

class Revenue(models.Model):
    nid = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="公司名称")
    project = models.ForeignKey(Project, to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="项目")
    income_name = models.CharField(max_length=64, verbose_name="收入名称", blank=True, null=True)
    income_classify = models.ForeignKey('Income_classify', to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="收入分类")
    number = models.CharField(max_length=64, verbose_name="存档编号", blank=True, null=True)
    coordinate = models.CharField(max_length=128, verbose_name="存档坐标", blank=True, null=True)
    money = models.DecimalField(max_digits=20, decimal_places=5, verbose_name="收入金额", blank=True, null=True)
    associates = models.ForeignKey(Staff, to_field='sid', on_delete=models.CASCADE, db_constraint=False, verbose_name="关联人")
    approver = models.ForeignKey('Approver2', to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="审批人")  # 数据库里有重复
    income_time = models.DateTimeField(auto_now_add=True, verbose_name="收入日期")
    remark = models.TextField(max_length=512, verbose_name="备注", blank=True, null=True)
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = "revenue"
        verbose_name = "收支管理"
        verbose_name_plural = "收支管理"

    def __str__(self):
        return self.income_name

    _insert = ['company_id', 'project_id', 'income_name', 'income_classify_id', 'number', 'coordinate', 'money', 'associates_id' ,'approver_id', 'income_time', 'remark']

    _update = ['nid', 'company_id', 'project_id', 'income_name', 'income_classify_id', 'number', 'coordinate', 'money', 'associates_id', 'approver_id', 'income_time', 'remark']


class RevenueAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    sid = models.ForeignKey('Revenue', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='收支附件')
    attachment = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'revenue_attach'
        verbose_name = '收支附件'
        verbose_name_plural = '收支附件'

    def __str__(self):
        return "收支附件:{0}".format(self.sid)

    _update = ["nid", "attachment", "name", "description"]


class Income_classify(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='收入分类', blank=True, null=True)

    class Meta:
        db_table = "income_classify"
        verbose_name = "收入分类"
        verbose_name_plural = "收入分类"

    def __str__(self):
        return self.name

    _insert = ['name']

    _update = ['name']


class Associates(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='关联人', blank=True, null=True)

    class Meta:
        db_table = 'associates'
        verbose_name = '关联人'
        verbose_name_plural = '关联人'

    def __str__(self):
        return self.name

    _insert = ['name']

    _update = ['name']


class Approver2(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='审批人')

    class Meta:
        db_table = 'approver2'
        verbose_name = '审批人'
        verbose_name_plural = '审批人'

    def __str__(self):
        return self.name

    _insert = ['name']

    _update = ['name']


# 支出管理
class Disbursement(models.Model):
    nid = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="公司名称")
    project = models.ForeignKey(Project, to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="项目")
    disbursement_name = models.CharField(max_length=64, verbose_name="支出名称", blank=True, null=True)
    classify = models.ForeignKey('Income_classify', to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="支出分类")
    number = models.CharField(max_length=64, verbose_name="存档编号", blank=True, null=True)
    coordinate = models.CharField(max_length=128, verbose_name="存档坐标", blank=True, null=True)
    money = models.DecimalField(max_digits=20, decimal_places=5, verbose_name="支出金额", blank=True, null=True)
    associates = models.ForeignKey('Associates', to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="关联人")
    approver = models.ForeignKey('Approver2', to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="审批人")  # 数据库里有重复
    disbursement_time = models.DateTimeField(auto_now_add=True, verbose_name="支出日期")
    remark = models.TextField(max_length=512, verbose_name="备注", blank=True, null=True)
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')\

    class Meta:
        db_table = "disbursement"
        verbose_name = "收支管理"
        verbose_name_plural = "收支管理"

    def __str__(self):
        return self.disbursement_name

    _insert = ['company_id', 'project_id', 'disbursement_name', 'classify_id', 'number', 'coordinate', 'money', 'associates_id' ,'approver_id', 'disbursement_time', 'remark']

    _update = ['nid', 'company_id', 'project_id', 'disbursement_name', 'classify_id', 'number', 'coordinate', 'money', 'associates_id', 'approver_id', 'disbursement_time', 'remark']

# 支出附件
class DisburAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    sid = models.ForeignKey('Disbursement', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='支出附件')
    attachment = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'disbur_attach'
        verbose_name = '支出附件'
        verbose_name_plural = '支出附件'

    def __str__(self):
        return "支出附件:{0}".format(self.sid)

    _update = ["nid", "attachment", "name", "description"]

