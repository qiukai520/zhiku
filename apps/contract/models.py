from django.db import models
from datetime import datetime
from sfa.models import CustomerInfo

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




# Create your models here.

# class Contract(models.Model):
#     number = models.CharField(max_length=50, verbose_name='合同编号')
#     name = models.CharField(max_length=50, verbose_name='合同名称', db_index=True)
#     supplier = models.CharField(max_length=50, verbose_name='供应商名称', db_index=True)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='contracts', verbose_name='公司',
#                                 default=1)
#     subject = models.ForeignKey(Subject, related_name='contracts', on_delete=models.CASCADE, verbose_name='合同类别')
#     sign = models.DateField(verbose_name='签订时间')
#     amount = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='初始金额')
#     definite = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='决算金额', blank=True, null=True)
#     active = models.BooleanField(default=True, verbose_name='有效')
#     is_cost = models.BooleanField(default=True,verbose_name='是否进成本')
#     jgc = models.BooleanField(default=False, verbose_name='甲供材')
#     text = models.TextField(blank=True, null=True, verbose_name='合同条款摘要')
#     master = models.PositiveIntegerField(null=True, blank=True, verbose_name='补充合同')
#     stamp = models.ForeignKey(Stamp, on_delete=models.CASCADE, related_name='contracts', verbose_name='印花税类型',
#                               default=12)
#     created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
#     updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('contracts:contract_detail', args=[self.id])
#
#     def hassupple(self):
#         supple = Contract.objects.filter(master=self.id).count()
#         return supple != 0
#
#     def is_supple(self):
#         return True if self.master else False
#
#     def master_contract(self):
#         if self.is_supple():
#             return get_object_or_404(Contract, id=int(self.master))
#         else:
#             return None
#
#     def supple_contracts(self):
#         if self.hassupple():
#             return Contract.objects.filter(master=self.id)
#         return None
#
#     def total_requisition(self):
#         if self.requisitions.all().count():
#             reqs = self.requisitions.all().aggregate(Sum('amount'))['amount__sum']
#             return reqs
#         else:
#             return None
#
#     def requisition_rate(self):
#         if self.definite and self.total_requisition():
#             return self.total_requisition() / self.definite
#         elif self.amount and self.total_requisition():
#             return self.total_requisition() / self.amount
#         else:
#             return None
#
#     def total_payment(self):
#         if self.payments.all().count():
#             return self.payments.all().aggregate(Sum('amount'))['amount__sum']
#         else:
#             return None
#
#     def payment_rate(self):
#         if self.total_payment() and self.definite:
#             return self.total_payment()/self.definite
#         elif self.total_payment() and self.amount:
#             return self.total_payment() / self.amount
#         else:
#             return None
#
#
#     class Meta:
#         ordering = ('subject','index', 'created')
#         verbose_name = '合同'
#         verbose_name_plural = '合同'
#
#


# 客户合同
# class Contract (SoftDeletableModel):
#     nid = models.AutoField(primary_key=True)
#     number = models.CharField(max_length=50, verbose_name='合同编号')
#     customer = models.ForeignKey(CustomerInfo, verbose_name=u"客户",on_delete=models.CASCADE)
#     product = models.ForeignKey("Product", verbose_name=u"产品", on_delete=models.CASCADE)
#     # subject = models.ForeignKey(Subject, related_name='contracts', on_delete=models.CASCADE, verbose_name='合同类别')
#     sign = models.DateField(verbose_name='签订时间')
#     amount = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='初始金额')
#     definite = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='决算金额', blank=True, null=True)
#     start_date = models.DateTimeField(verbose_name=u"生效时间", default=datetime.now)
#     end_date = models.DateTimeField(verbose_name=u"到期时间", default=datetime.now)
#     content = models.TextField(verbose_name=u"备注", blank=True)
#     is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
#     create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
#     last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')
#
#     class Meta:
#        verbose_name = u"客户合同"
#        verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return str(self.number)
#
#
# class Product(SoftDeletableModel):
#     nid = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=64, verbose_name='产品名称')
#
#     class Meta:
#         verbose_name = u"产品"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return str(self.name)
