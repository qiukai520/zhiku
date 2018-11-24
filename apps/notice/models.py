from django.db import models
from personnel.models import Staff
import django.utils.timezone as timezone


# Create your models here.
NOTICE_TYPE = (
    ('notice', '系统消息'),
    ('inform', '任务通知'),
)


class Notice(models.Model):
    nid = models.AutoField(primary_key=True)
    notice_title = models.CharField('通知标题', max_length=30)
    notice_body = models.TextField('通知内容')
    notice_url = models.CharField('父链接', max_length=50, null=True)
    notice_type = models.CharField('通知类型', max_length=30, choices=NOTICE_TYPE)
    notice_time = models.DateTimeField('通知时间', default=timezone.now)
    user = models.ForeignKey(Staff,to_field="sid", related_name='notice_for_user', verbose_name=u'所属用户',
                                    on_delete = models.CASCADE)
    notice_status = models.BooleanField('阅读状态', default=False)

    class Meta:
        db_table = 'notice'
        verbose_name = '通知'
        verbose_name_plural = '通知'

    def __str__(self):
        return self.notice_title
