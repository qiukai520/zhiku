from django.db import models
from personnel.models import Company, Project
from revenue.models import Approver2
# Create your models here.

class AssetsClassify(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='分类', blank=True, null=True)

    class Meta:
        db_table = 'assetsclassify'
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    _insert = ['name']

    _update = ['name']

class SaveCoordinate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='存档坐标', blank=True, null=True)

    class Meta:
        db_table = 'save_coordinate'
        verbose_name = '存档坐标'
        verbose_name_plural = '存档坐标'

    def __str__(self):
        return self.name

    _insert = ['name']

    _update = ['name']

class ProcurementName(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='采购人', blank=True, null=True)

    class Meta:
        db_table = 'procurement_name'
        verbose_name = '采购人'
        verbose_name_plural = '采购人'

    def __str__(self):
        return self.name

    _insert = ['name']

    _update = ['name']

class UserName(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='使用人')

    class Meta:
        db_table = 'user_name'
        verbose_name = '使用人'
        verbose_name_plural = '使用人'

    def __str__(self):
        return self.name

    _insert = ['name']

    _update = ['name']

class AssetsStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='资产状态')

    class Meta:
        db_table = 'assets_status'
        verbose_name = '资产状态'
        verbose_name_plural = '资产状态'

    def __str__(self):
        return self.name

    _insert = ['name']

    _update = ['name']

class Assets(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15, blank=True, null=True, verbose_name="名称")
    assets_classify = models.ForeignKey("AssetsClassify", to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="分类")
    save_number = models.CharField(max_length=32, blank=True, null=True, verbose_name="存档编号")
    save_coordinate = models.ForeignKey("SaveCoordinate", to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="存档坐标")
    quantity = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True, verbose_name="数量")
    procurement_time = models.DateTimeField(auto_now_add=True, verbose_name="采购日期")
    procurement_money = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="采购金额")
    procurement_name = models.ForeignKey("ProcurementName", to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="采购人")
    invoice = models.CharField(max_length=32, blank=True, null=True, verbose_name="发票")
    user_name = models.ForeignKey("UserName", to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="使用人")
    evidence = models.CharField(max_length=32, blank=True, null=True, verbose_name="领取凭据")
    evidence_number = models.CharField(max_length=32, blank=True, null=True, verbose_name="凭据存档编号")
    company = models.ForeignKey(Company, to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="隶属公司")
    project = models.ForeignKey(Project, to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="隶属项目")
    assets_status = models.ForeignKey("AssetsStatus", to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="资产状态")
    approver = models.ForeignKey(Approver2, to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name="审批人")
    remark = models.TextField(max_length=512, blank=True, null=True, verbose_name="备注")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = "assets"
        verbose_name = "资产管理"
        verbose_name_plural = "资产管理"

    def __str__(self):
        return self.name

    _insert = ['name', 'assets_classify_id', 'save_number', 'save_coordinate_id', 'quantity', 'procurement_time', 'procurement_money', 'procurement_name_id', 'invoice', 'user_name_id',
                'evidence', 'evidence_number', 'company_id', 'project_id', 'assets_status_id', 'approver_id', 'remark']

    _update = ['nid', 'name', 'assets_classify_id', 'save_number', 'save_coordinate_id', 'quantity', 'procurement_time', 'procurement_money', 'procurement_name_id', 'invoice', 'user_name_id',
                'evidence', 'evidence_number', 'company_id', 'project_id', 'assets_status_id', 'approver_id', 'remark']

class AssetsAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    sid = models.ForeignKey('Assets', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='资产附件')
    attachment = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'assets_attach'
        verbose_name = '资产附件'
        verbose_name_plural = '资产附件'

    def __str__(self):
        return "资产附件:{0}".format(self.sid)

    _update = ["nid", "attachment", "name", "description"]