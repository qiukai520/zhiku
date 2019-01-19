from django.db import models
from public.managers import SoftDeletableManager

from contract.models import ContractInfo
from personnel.models import Staff
from sfa.models import FollowWay,FollowContact,CustomerLinkman
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


class ContractFollow(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    contract = models.ForeignKey(ContractInfo, to_field="nid", on_delete=models.CASCADE, db_constraint=False,
                                 default=1, verbose_name='合同')
    way = models.ForeignKey(FollowWay, to_field='nid', on_delete=models.CASCADE, db_constraint=False,verbose_name="跟进方式")
    contact = models.ForeignKey(FollowContact, to_field='nid', on_delete=models.CASCADE, db_constraint=False, verbose_name="联络方式")
    linkman = models.ForeignKey(CustomerLinkman, to_field='nid', on_delete=models.CASCADE, db_constraint=False, verbose_name="联系人")
    detail = models.TextField(max_length=512, blank=True, null=True, verbose_name="跟进详情")
    next_step = models.TextField(max_length=512, blank=True,null=True,verbose_name="下一步跟进计划")
    recorder = models.ForeignKey(Staff, to_field='sid', on_delete=models.CASCADE, db_constraint=False, verbose_name="登记人")
    date = models.DateField(verbose_name="跟进日期")
    is_deleted = models.BooleanField(default=False,verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'contract_follow'
        verbose_name = '合同跟进记录'
        verbose_name_plural = '合同跟进记录'

    def __str__(self):
        return "合同跟进记录:{0}".format(self.contract)

    _insert = ["recorder_id","date", "way_id", "contract_id", "contact_id", "linkman_id","next_step","detail"]
    _update = ["recorder_id","date","way_id","contract_id", "contact_id", "linkman_id","next_step","detail"]


class ContractFollowAttach(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    follow = models.ForeignKey('ContractFollow', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='合同跟进')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'contract_follow_attach'
        verbose_name = '合同跟进附件'
        verbose_name_plural = '合同跟进附件'

    def __str__(self):
        return "合同跟进附件:{0}".format(self.name)