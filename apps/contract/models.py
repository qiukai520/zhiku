from django.db import models
from datetime import datetime
from sfa.models import CustomerInfo
from personnel.models import Staff
from django.db import models
from django.db.models.query import QuerySet
from public.managers import SoftDeletableManager

# Create your models here.

# 自定义软删除抽象基类


class SoftDeletableModel(models.Model):
    """
    An abstract base class model with a ``is_deleted`` field that
    marks entries that are not going to be used anymore, but are
    kept in db for any reason.
    Default manager returns only not-deleted entries.
    """
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    objects = SoftDeletableManager()

    def delete(self, using=None, soft=True, *args, **kwargs):
        """
        Soft delete object (set its ``is_deleted`` field to True).
        Actually delete object if setting ``soft`` to False.
        """
        if soft:
            self.is_deleted = True
            self.save(using=using)
        else:
            return super(SoftDeletableModel, self).delete(using=using, *args, **kwargs)


class ContractInfo(SoftDeletableModel):
    approved_choice = ((0, '未审核'),(1, '通过'), (2, '驳回'))

    nid = models.AutoField(primary_key=True)
    identifier = models.CharField(max_length=50, verbose_name='合同编号')
    customer = models.ForeignKey(CustomerInfo, verbose_name=u"客户", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", verbose_name=u"产品", on_delete=models.CASCADE)
    product_meal = models.ForeignKey("ProductMeal", verbose_name=u"套餐", on_delete=models.CASCADE)
    remark = models.TextField(verbose_name=u"备注", blank=True)
    year_limit = models.SmallIntegerField(verbose_name="年限")
    received = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="应收金额", blank=True, null=True)
    receivable = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="应收金额", blank=True, null=True)
    pending = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="待收金额", blank=True, null=True)
    sign = models.DateField(verbose_name='签订时间')
    belonger = models.ForeignKey(Staff, to_field="sid", on_delete=models.CASCADE, verbose_name='签订人',
                                 db_constraint=False)
    follower = models.ForeignKey(Staff,blank=True, null=True, to_field="sid", related_name="fol_crt", on_delete=models.CASCADE, verbose_name='跟进客服',
                                 db_constraint=False)
    helper = models.ForeignKey(Staff, to_field="sid", related_name='helper', blank=True, null=True, on_delete=models.CASCADE, verbose_name='辅助人',
                                 db_constraint=False)
    start_date = models.DateTimeField(verbose_name=u"生效时间", default=datetime.now)
    end_date = models.DateTimeField(verbose_name=u"到期时间", default=datetime.now)
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    location = models.ForeignKey('ContractLocation', to_field="nid", blank=True, null=True, on_delete=models.CASCADE,
                                 db_constraint=False, verbose_name='存放坐标')
    is_approved = models.SmallIntegerField(choices=approved_choice, default=0, verbose_name="审批状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'contract_info'
        verbose_name = u"合同信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.identifier)

    _insert = ["identifier","customer_id", "location_id", "product_id","year_limit", "belonger_id","helper_id","product_meal_id","remark","received","receivable","pending","sign",
               "end_date","start_date"]
    _update = ["identifier","customer_id", "location_id","product_id","year_limit","product_meal_id","belonger_id","helper_id","remark","received","receivable","pending","sign",
               "end_date","start_date"]


class ProductMeal(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    product = models.ForeignKey("Product", verbose_name=u"产品", on_delete=models.CASCADE)
    name = models.CharField(max_length=64, verbose_name='套餐名称')
    standard = models.CharField(max_length=32,verbose_name="规格")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="价格")
    year_limit = models.SmallIntegerField(verbose_name="年限")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'product_meal'
        verbose_name = u"产品套餐"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)
    _insert = ["name","product_id","standard","price","year_limit"]
    _update = ["name","product_id","standard","price","year_limit"]


class Product(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name='产品名称')
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'product'
        verbose_name = u"产品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)

    _insert = ["name"]
    _update = ["name"]


class ContractLocation(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    location = models.CharField(max_length=64, verbose_name="坐标")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'contract_location'
        verbose_name = u"合同存档坐标"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.location)

    _insert = ["location"]
    _update = ["location"]


class ContractAttach(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    contract = models.ForeignKey('ContractInfo', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='合同')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        db_table = 'contract_attach'
        verbose_name = '合同附件'
        verbose_name_plural = '合同附件'

    def __str__(self):
        return "合同附件:{0}".format(self.name)


class Approver(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    approver = models.ForeignKey(Staff, to_field="sid", on_delete=models.CASCADE, verbose_name=u"审批人")
    follow = models.SmallIntegerField(verbose_name=u"审批顺序")  # 0代表无顺序
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        db_table = "approver"
        verbose_name = u"合同审批人"
        verbose_name_plural = verbose_name


class ApproverResult(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    contract = models.ForeignKey('ContractInfo', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                                 verbose_name='合同')
    approver = models.ForeignKey(Staff, to_field="sid", on_delete=models.CASCADE, verbose_name=u"审批人")
    follow = models.SmallIntegerField(verbose_name=u"审批顺序")  # 0代表无顺序
    result = models.SmallIntegerField(verbose_name=u"审批结果")  # 0未审核，1通过，2不通过
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        db_table = "approver_result"
        verbose_name = "合同审核结果"
        verbose_name_plural = verbose_name


class ApproverRecord(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    result = models.ForeignKey('ApproverResult', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                                 verbose_name='审核结果')
    content = models.CharField(max_length=128, verbose_name="内容")
    result2 = models.SmallIntegerField(verbose_name=u"当前审批结果")  # 0未审核，1通过，2不通过
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        db_table = "approver_record"
        verbose_name = "合同审核记录"
        verbose_name_plural = verbose_name

    _insert = ["content", "result2"]
    _update = ["content", "result2"]



class ContractPayment(SoftDeletableModel):
    """合同尾款"""
    approved_choice = ((0, '未审核'),(1, '通过'), (2, '驳回'))
    nid = models.AutoField(primary_key=True)
    contract = models.ForeignKey('ContractInfo', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                                 verbose_name='合同')
    payment = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="收款金额")
    date = models.DateTimeField(verbose_name=u"收款时间", default=datetime.now)
    remark = models.TextField(verbose_name=u"备注", blank=True)
    is_approved = models.SmallIntegerField(choices=approved_choice, default=0, verbose_name="审批状态")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'contract_payment'
        verbose_name = u"合同尾款"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "合同尾款{0}:{1}".format(self.contract,self.nid)

    _update = ["payment","contract_id","remark","date"]

    _insert = ["payment","contract_id","remark","date"]


class PaymentAttach(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    payment = models.ForeignKey('ContractPayment', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='合同尾款')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        db_table = 'payment_attach'
        verbose_name = '尾款附件'
        verbose_name_plural = '尾款附件'

    def __str__(self):
        return "尾款附件:{0}".format(self.name)


class PaymentApprove(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    payment = models.ForeignKey('ContractPayment', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                                 verbose_name='尾款')
    approver = models.ForeignKey(Staff, to_field="sid", on_delete=models.CASCADE, verbose_name=u"审批人")
    follow = models.SmallIntegerField(verbose_name=u"审批顺序")  # 0代表无顺序
    result = models.SmallIntegerField(verbose_name=u"审批结果")  # 0未审核，1通过，2不通过
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        db_table = "payment_approve"
        verbose_name = "尾款审核结果"
        verbose_name_plural = verbose_name


class PaymentApproveRecord(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    result = models.ForeignKey('PaymentApprove', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                                 verbose_name='尾款审核结果')
    content = models.CharField(max_length=128, verbose_name="内容")
    result2 = models.SmallIntegerField(verbose_name=u"当前审批结果")  # 0未审核，1通过，2不通过
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        db_table = "payment_approve_record"
        verbose_name = "尾款审核记录"
        verbose_name_plural = verbose_name

    _insert = ["content", "result2"]
    _update = ["content", "result2"]