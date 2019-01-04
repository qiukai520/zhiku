from django.db import models
from public.managers import SoftDeletableManager
from task.models import Task,TaskType
from personnel.models import Staff

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

class CollAttachment(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    tsid = models.ForeignKey('CollRecord', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                             verbose_name='收录内容')
    attachment = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件描述')
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        db_table = 'coll_attach'
        verbose_name = '收录相关附件'
        verbose_name_plural = '收录相关附件'


class CollRecord(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    tid = models.ForeignKey(Task, to_field="tid", on_delete=models.CASCADE, verbose_name='任务',
                            db_constraint=False)
    origin = models.IntegerField(verbose_name="原数据")
    title = models.CharField(max_length=512, blank=True, null=True, verbose_name="标题")
    summary = models.CharField(max_length=512, blank=True, null=True, verbose_name='小结')
    remark = models.CharField(max_length=512, blank=True, null=True, verbose_name='备注')
    tag = models.CharField(max_length=128, blank=True, null=True, verbose_name='标签')
    relate_tag = models.CharField(max_length=128, blank=True, null=True, verbose_name='关联标签')
    relate_title = models.CharField(max_length=128, blank=True, null=True, verbose_name='关联标题')
    industry = models.CharField(max_length=64,blank=True,null=True,verbose_name="关联行业")
    recorder = models.ForeignKey(Staff, to_field="sid",  blank=True, null=True,
                               on_delete=models.CASCADE, verbose_name='收录人',
                               db_constraint=False)
    type = models.ForeignKey(TaskType, to_field="tpid", on_delete=models.CASCADE, verbose_name='任务类型',
                             db_constraint=False, default=1)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    favor = models.IntegerField(verbose_name="点赞数")
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        db_table = 'coll_record'
        verbose_name = '收录内容'
        verbose_name_plural = '收录内容'

    def __str__(self):
        return '收录内容{0}'.format(self.title)
