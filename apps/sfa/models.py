from django.db import models
from django.db.models.query import QuerySet
from .managers import SoftDeletableManager
from inventory.models import Industry
from public.models import Town
from personnel.models import Staff,JobTitle
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


class CustomerInfo(SoftDeletableModel):

    delete_choice = ((0, '保留'), (1, '删除'))
    nid = models.AutoField(primary_key=True)
    category = models.ForeignKey("CustomerCategory", to_field="nid", on_delete=models.CASCADE, verbose_name='客户分类',
                                 db_constraint=False)
    purpose = models.ForeignKey("CustomerPurpose", to_field='nid', on_delete=models.CASCADE, db_constraint=False, verbose_name="客户意向")
    company = models.CharField(max_length=64, verbose_name="公司名称")
    industry = models.ForeignKey(Industry, to_field="nid", on_delete=models.CASCADE, verbose_name='行业',
                                 db_constraint=False)
    business = models.CharField(max_length=64, verbose_name="主营业务" )
    employees = models.IntegerField(verbose_name='公司人数')
    introduce = models.CharField(max_length=512, verbose_name="简介", blank=True, null=True)
    website = models.CharField(max_length=64, verbose_name="网站", blank=True, null=True)
    phone = models.CharField(max_length=16, verbose_name="联系电话", blank=True, null=True)
    town = models.ForeignKey(Town, to_field="nid", on_delete=models.CASCADE, verbose_name='街道',
                               db_constraint=False)
    address = models.CharField(max_length=64, verbose_name="地址", blank=True, null=True)
    remark = models.TextField(max_length=512, verbose_name="备注", blank=True, null=True)
    follower = models.ForeignKey(Staff,blank=True, null=True, to_field="sid", related_name="customer_follower", on_delete=models.CASCADE, verbose_name='跟进人',
                                 db_constraint=False)
    ftime = models.DateTimeField(auto_now_add=True, verbose_name='开始跟进时间')
    recorder = models.ForeignKey(Staff, to_field="sid", on_delete=models.CASCADE, verbose_name='记录人',
                                 db_constraint=False)
    is_sign = models.BooleanField(default=False,verbose_name="是否签约")
    is_deleted = models.BooleanField(default=False,verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'customer_info'
        verbose_name = '客户信息'
        verbose_name_plural = '客户信息'

    def __str__(self):
        return self.company

    _insert = ["purpose_id","company" ,"category_id","follower_id","recorder_id","industry_id", "business""employees","introduce",'website',"remark","address",
                "town_id", "phone"]
    _update = ["purpose_id","company","category_id","follower_id", "industry_id", "business","employees","introduce",'website',"remark","address",
                "town_id","phone"]


class CustomerCategory(models.Model):
    nid = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=16,verbose_name="类别")

    class Meta:
        db_table = 'customer_category'
        verbose_name = '客户分类'
        verbose_name_plural = '客户分类'

    def __str__(self):
        return self.caption

    _insert = ["caption"]
    _update = ["caption"]


class CustomerAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    customer = models.ForeignKey('CustomerInfo', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='客户')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'customer_attach'
        verbose_name = '客户附件'
        verbose_name_plural = '客户附件'

    def __str__(self):
        return "客户附件:{0}".format(self.name)


class CustomerLicence(models.Model):
    nid = models.AutoField(primary_key=True)
    customer = models.ForeignKey('CustomerInfo', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='客户')
    photo = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')

    class Meta:
        db_table = 'customer_licence'
        verbose_name = '客户营业执照'
        verbose_name_plural = '客户营业执照'

    def __str__(self):
        return "营业执照:{0}".format(self.name)

    _update = ["photo","name"]


class CustomerPhoto(models.Model):
    nid = models.AutoField(primary_key=True)
    customer = models.ForeignKey('CustomerInfo', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='客户')
    photo = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')

    class Meta:
        db_table = 'customer_photo'
        verbose_name = '客户照片'
        verbose_name_plural = '客户照片'

    def __str__(self):
        return "客户照片:{0}".format(self.name)

    _update = ["photo","name"]


class CustomerLinkman(SoftDeletableModel):
    gender_choice = ((0, "男"), (1, "女"))
    marriage_choice = ((0, "未婚"), (1, "已婚"))
    delete_status_choice = ((0, '删除'), (1, '保留'))
    is_lunar = ((0, "公历"), (1, "农历"))

    nid = models.AutoField(primary_key=True)
    customer = models.ForeignKey('CustomerInfo', to_field="nid", on_delete=models.CASCADE, db_constraint=False,
                                   default=1, verbose_name='客户')
    name = models.CharField(max_length=32, verbose_name='姓名')
    wx_name = models.CharField(max_length=32, verbose_name='微信名')
    gender = models.SmallIntegerField(choices=gender_choice, verbose_name="性别", default=0)
    age = models.SmallIntegerField(verbose_name="年龄", blank=True, null=True)
    job_title = models.ForeignKey(JobTitle, to_field="id", on_delete=models.CASCADE, db_constraint=False,
                                verbose_name='职称', blank=True, null=True)
    marriage = models.SmallIntegerField(choices=marriage_choice, verbose_name="婚姻", default=0)
    mobile = models.CharField(max_length=11, verbose_name="手机号码", blank=True, null=True)
    phone = models.CharField(max_length=16, verbose_name="电话", blank=True, null=True)
    ext_phone = models.CharField(max_length=16, verbose_name="分机", blank=True, null=True)
    birthday = models.DateField(verbose_name="生日", blank=True, null=True)
    is_lunar = models.SmallIntegerField(choices=is_lunar, verbose_name="生日农历or公历", default=0)
    native_place = models.CharField(max_length=64, verbose_name="籍贯", blank=True, null=True)
    is_deleted = models.BooleanField(default=False,verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'customer_linkman'
        verbose_name = '联系人'
        verbose_name_plural = '联系人'

    def __str__(self):
            return self.name

    _insert = ["customer_id", "name", "gender","job_title_id" ,"age", "marriage", "mobile", "phone", "ext_phone",
               "birthday","is_lunar","native_place","wx_name"]
    _update = ["customer_id", "name", "gender", "age","job_title_id", "marriage", "mobile", "phone", "ext_phone",
               "birthday","is_lunar","native_place","wx_name"]


class CustomerLinkmanAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    linkman = models.ForeignKey('CustomerLinkman', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='联系人')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'customer_linkman_attach'
        verbose_name = '联系人附件'
        verbose_name_plural = '联系人附件'

    def __str__(self):
        return "联系人附件:{0}".format(self.name)


class CustomerLinkmanCard(models.Model):
    nid = models.AutoField(primary_key=True)
    linkman = models.ForeignKey("CustomerLinkman", to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='联系人')
    photo = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')

    class Meta:
        db_table = 'customer_linkman_card'
        verbose_name = '联系人名片'
        verbose_name_plural = '联系人名片'

    def __str__(self):
        return "联系人名片:{0}".format(self.name)

    _update = ["photo","name"]


class CustomerLinkmanPhoto(models.Model):
    nid = models.AutoField(primary_key=True)
    linkman = models.ForeignKey('CustomerLinkman', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='联系人')
    photo = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')

    class Meta:
        db_table = 'customer_linkman_photo'
        verbose_name = '联系人图片'
        verbose_name_plural = '联系人图片'

    def __str__(self):
        return "联系人图片:{0}".format(self.name)

    _update = ["photo","name"]


class CustomerMemo(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    customer = models.ForeignKey('CustomerInfo', to_field="nid", on_delete=models.CASCADE, db_constraint=False,
                                 default=1, verbose_name='客户')
    title = models.CharField(max_length=16,verbose_name="标题")
    detail = models.CharField(max_length=16,verbose_name="详细")
    recorder = models.ForeignKey(Staff, to_field="sid", on_delete=models.CASCADE, verbose_name='登记人',
                                 db_constraint=False)
    is_deleted = models.BooleanField(default=False,verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'customer_memo'
        verbose_name = '客户备忘'
        verbose_name_plural = '客户备忘'

    def __str__(self):
        return self.title

    _insert = ["customer_id","title",'detail',"recorder_id"]
    _update = ["customer_id","title",'detail',"recorder_id"]


class CustomerMemoAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    memo = models.ForeignKey('CustomerMemo', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='客户备忘')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'customer_memo_attach'
        verbose_name = '备忘附件'
        verbose_name_plural = '备忘附件'

    def __str__(self):
        return "备忘附件:{0}".format(self.name)


class FollowWay(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    code = models.CharField(max_length=16, verbose_name='算法编号')
    content = models.TextField(max_length=128, verbose_name='跟进方式')
    is_deleted = models.BooleanField(default=False,verbose_name="是否删除")


    class Meta:
        db_table = 'follow_way'
        verbose_name = '跟进方式'
        verbose_name_plural = '跟进方式'

    def __str__(self):
        return "跟进方式:{0}".format(self.code)

    _insert = ["code", "content",]
    _update = ["customer_id", "title", 'detail', "recorder_id"]


class FollowContact(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    code = models.CharField(max_length=16, verbose_name='算法编号')
    content = models.TextField(max_length=128, verbose_name='联络方式')
    is_deleted = models.BooleanField(default=False,verbose_name="是否删除")


    class Meta:
        db_table = 'follow_contact'
        verbose_name = '联络方式'
        verbose_name_plural = '联络方式'

    def __str__(self):
        return "联络方式:{0}".format(self.code)


class FollowResult(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    code = models.CharField(max_length=16, verbose_name='算法编号')
    content = models.TextField(max_length=128, verbose_name='需求意向')
    is_deleted = models.BooleanField(default=False,verbose_name="是否删除")


    class Meta:
        db_table = 'follow_result'
        verbose_name = '客户意向'
        verbose_name_plural = '客户意向'

    def __str__(self):
        return "客户意向:{0}".format(self.code)


class CustomerPurpose(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    code = models.CharField(max_length=16, verbose_name='算法编号')
    content = models.TextField(max_length=128, verbose_name='客户意向')
    is_deleted = models.BooleanField(default=False,verbose_name="是否删除")


    class Meta:
        db_table = 'customer_purpose'
        verbose_name = '意向分类'
        verbose_name_plural = '意向分类'

    def __str__(self):
        return "意向分类:{0}".format(self.code)


class CustomerFollow(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    customer = models.ForeignKey('CustomerInfo', to_field="nid", on_delete=models.CASCADE, db_constraint=False,
                                 default=1, verbose_name='客户')
    way = models.ForeignKey("FollowWay", to_field='nid', on_delete=models.CASCADE, db_constraint=False,verbose_name="跟进方式")
    contact = models.ForeignKey("FollowContact", to_field='nid', on_delete=models.CASCADE, db_constraint=False, verbose_name="联络方式")
    linkman = models.ForeignKey("CustomerLinkman", to_field='nid', on_delete=models.CASCADE, db_constraint=False, verbose_name="联系人")
    result = models.ForeignKey("FollowResult", to_field='nid', on_delete=models.CASCADE, db_constraint=False, verbose_name="需求意向")
    purpose = models.ForeignKey("CustomerPurpose", to_field='nid', on_delete=models.CASCADE, db_constraint=False, verbose_name="客户意向")
    detail = models.TextField(max_length=512, blank=True, null=True, verbose_name="跟进详情")
    next_step = models.TextField(max_length=512, blank=True,null=True,verbose_name="下一步跟进计划")
    recorder = models.ForeignKey(Staff, to_field='sid', on_delete=models.CASCADE, db_constraint=False, verbose_name="登记人")
    date = models.DateField(verbose_name="跟进日期")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'customer_follow'
        verbose_name = '客户跟进记录'
        verbose_name_plural = '客户跟进记录'

    def __str__(self):
        return "客户跟进记录:{0}".format(self.customer)

    _insert = ["recorder_id","date", "way_id", "customer_id", "contact_id", "linkman_id","result_id","purpose_id","next_step","detail"]
    _update = ["recorder_id","date","way_id","customer_id", "contact_id", "linkman_id","result_id","purpose_id","next_step","detail"]


class CustomerFollowAttach(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    follow = models.ForeignKey('CustomerFollow', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='客户跟踪')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'c_follow_attach'
        verbose_name = '客户跟踪附件'
        verbose_name_plural = '客户跟踪附件'

    def __str__(self):
        return "客户跟踪附件:{0}".format(self.name)


class CustomerContact(SoftDeletableModel):
    delete_status_choice = ((0, '删除'), (1, '保留'))
    category = ((0, "交易收入"), (1, "商务支出"))
    nid = models.AutoField(primary_key=True)
    customer = models.ForeignKey('CustomerInfo', to_field="nid", on_delete=models.CASCADE, db_constraint=False,
                             default=1, verbose_name='客户')
    linkman = models.ForeignKey('CustomerLinkman', to_field="nid", on_delete=models.CASCADE, db_constraint=False,
                                 default=1, verbose_name='联系人')
    category = models.SmallIntegerField(choices=category, verbose_name="分类", default=0)
    project = models.CharField(max_length=64, verbose_name="项目名称", blank=True, null=True)
    description = models.CharField(max_length=128, verbose_name="项目详细", blank=True, null=True)
    received = models.DecimalField(max_digits=8, decimal_places=2,verbose_name="已收/已付金额",blank=True,null=True)
    received_remark = models.CharField(max_length=64, verbose_name="已收/已付备注", blank=True, null=True)
    receivable = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="应收/应付金额", blank=True, null=True)
    receivable_remark = models.CharField(max_length=64,verbose_name="应收/应付备注", blank=True, null=True)
    pending = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="待收/待付金额", blank=True, null=True)
    pending_remark = models.CharField(max_length=64, verbose_name="待收/待付备注",blank=True,null=True)
    date = models.DateField(verbose_name="交易日期", blank=True, null=True)
    is_deleted = models.BooleanField(default=False,verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'customer_contact'
        verbose_name = '客户来往'
        verbose_name_plural = '客户来往'

    def __str__(self):
        return self.project

    _insert = ["customer_id", "linkman_id", "company", 'project',"description", "category", "received", "received_remark",
               "receivable", "receivable_remark","pending","pending_remark","date"]

    _update = ["customer_id", "linkman_id", "company",'project',"description", "category", "received", "received_remark",
               "receivable", "receivable_remark","pending","pending_remark","date"]


class ContactAttach(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    contact = models.ForeignKey('CustomerContact', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='客户来往')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')
    is_deleted = models.BooleanField(default=False,verbose_name="是否删除")

    class Meta:
        db_table = 'c_contact_attach'
        verbose_name = '来往附件'
        verbose_name_plural = '来往附件'

    def __str__(self):
        return "来往附件:{0}".format(self.name)


class SeaRule(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    rule = models.SmallIntegerField(verbose_name="公海规则", default=15)
    is_deleted = models.BooleanField(default=False,verbose_name="是否删除")

    class Meta:
        db_table = 'sea_rule'
        verbose_name = '公海规则'
        verbose_name_plural = '公海规则'

    def __str__(self):
        return "公海规则:{0}".format(self.rule)

    _update = ["rule"]
    _insert = ["rule"]







