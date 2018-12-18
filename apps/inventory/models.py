from django.db import models
from personnel.models import Staff
from public.models import Town
from personnel.models import JobTitle
# Create your models here.


class Supplier(models.Model):
    delete_status_choice = ((0, '删除'), (1, '保留'))
    nid = models.AutoField(primary_key=True)
    category = models.ForeignKey("SupplierCategory", to_field="nid", on_delete=models.CASCADE, verbose_name='供应商分类',
                               db_constraint = False)
    company = models.CharField(max_length=64,verbose_name="公司名称")
    industry = models.ForeignKey("Industry", to_field="nid", on_delete=models.CASCADE, verbose_name='行业',
                               db_constraint = False)
    employees = models.IntegerField(verbose_name='公司人数')
    products = models.CharField(max_length=64, verbose_name="主营商品")
    introduce = models.CharField(max_length=512, verbose_name="简介", blank=True, null=True)
    website = models.CharField(max_length=64, verbose_name="网站", blank=True, null=True)
    phone = models.CharField(max_length=16, verbose_name="联系电话", blank=True, null=True)
    bank = models.CharField(max_length=512, verbose_name="开户银行", blank=True, null=True)
    bank_account = models.CharField(max_length=512, verbose_name="银行账户", blank=True, null=True)
    account_name = models.CharField(max_length=512, verbose_name="账户名", blank=True, null=True)
    town = models.ForeignKey(Town, to_field="nid", on_delete=models.CASCADE, verbose_name='街道',
                               db_constraint = False)
    address = models.CharField(max_length=64, verbose_name="地址", blank=True, null=True)
    remark = models.CharField(max_length=512, verbose_name="备注", blank=True, null=True)
    delete_status = models.SmallIntegerField(choices=delete_status_choice, default=1, verbose_name='删除状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'supplier'
        verbose_name = '供应商'
        verbose_name_plural = '供应商'

    def __str__(self):
        return self.company

    _insert = [ "category_id","company","products", "industry_id", "employees","goods_id","introduce",'website',"remark","address",
                "town_id","account_name","bank_account","bank","phone"]
    _update = ["category_id", "company", "products","industry_id", "employees", "goods_id", "introduce", 'website', "remark", "address",
               "town_id", "account_name", "bank_account", "bank", "phone"]


class Goods(models.Model):
    delete_status_choice = ((0, '删除'), (1, '保留'))

    nid = models.AutoField(primary_key=True)
    category = models.ForeignKey("GoodsCategory", to_field="nid", on_delete=models.CASCADE, verbose_name='商品分类',
                               db_constraint=False)
    name = models.CharField(max_length=64,verbose_name="商品名称")
    description = models.CharField(max_length=256,verbose_name="描述", blank=True, null=True)

    unit = models.ForeignKey("GoodsUnit", to_field="nid", on_delete=models.CASCADE, verbose_name='商品单位',
                                 db_constraint=False)
    code = models.CharField(max_length=64, verbose_name="商品条码")
    standard = models.CharField(max_length=32, verbose_name='商品规格', blank=True, null=True)
    start_month = models.SmallIntegerField(blank=True, null=True, verbose_name='起始产期(月份)',)
    photo = models.CharField(max_length=1024, blank=True, null=True,verbose_name="图片路径")
    end_month = models.SmallIntegerField(blank=True, null=True, verbose_name='结束期(月份)')
    area = models.CharField(max_length=64, verbose_name='产地', blank=True, null=True)
    delete_status = models.SmallIntegerField(choices=delete_status_choice, default=1, verbose_name='删除状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'goods'
        verbose_name = '商品'
        verbose_name_plural = '商品'

    def __str__(self):
        return self.name
    _insert=["category_id","name","description","unit_id","code","standard","start_month","end_month","photo","area"]
    _update=["category_id","name","description","unit_id","code","standard","start_month","end_month","photo","area"]


class SupplierContact(models.Model):
    delete_status_choice = ((0, '删除'), (1, '保留'))
    category = ((0, "交易收入"), (1, "商务支出"))
    nid = models.AutoField(primary_key=True)
    supplier = models.ForeignKey('Supplier', to_field="nid", on_delete=models.CASCADE, db_constraint=False,
                             default=1, verbose_name='供应商')
    linkman = models.ForeignKey('Linkman', to_field="nid", on_delete=models.CASCADE, db_constraint=False,
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
    delete_status = models.SmallIntegerField(choices=delete_status_choice, default=1, verbose_name='删除状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'supplier_contact'
        verbose_name = '供应商来往'
        verbose_name_plural = '供应商来往'

    def __str__(self):
        return self.project

    _insert = ["supplier_id", "linkman_id", "company", 'project',"description", "category", "received", "received_remark",
               "receivable", "receivable_remark","pending","pending_remark","date"]

    _update = ["supplier_id", "linkman_id", "company",'project',"description", "category", "received", "received_remark",
               "receivable", "receivable_remark","pending","pending_remark","date"]


class ContactAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    contact = models.ForeignKey('SupplierContact', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='供应来往')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'contact_attach'
        verbose_name = '来往附件'
        verbose_name_plural = '来往附件'

    def __str__(self):
        return "来往附件:{0}".format(self.name)


class Linkman(models.Model):
    gender_choice = ((0, "男"), (1, "女"))
    marriage_choice = ((0, "未婚"), (1, "已婚"))
    delete_status_choice = ((0, '删除'), (1, '保留'))
    is_lunar = ((0, "公历"), (1, "农历"))

    nid = models.AutoField(primary_key=True)
    supplier = models.ForeignKey('Supplier', to_field="nid", on_delete=models.CASCADE, db_constraint=False,
                                   default=1, verbose_name='供应商')
    name = models.CharField(max_length=32, verbose_name='联系人')
    gender = models.SmallIntegerField(choices=gender_choice, verbose_name="性别", default=0)
    job_title = models.ForeignKey(JobTitle, to_field="id", on_delete=models.CASCADE, db_constraint=False,
                                  verbose_name='职称', blank=True, null=True)
    age = models.SmallIntegerField(verbose_name="年龄", blank=True, null=True)
    marriage = models.SmallIntegerField(choices=marriage_choice, verbose_name="婚姻", default=0)
    mobile = models.CharField(max_length=11, verbose_name="手机号码", blank=True, null=True)
    phone = models.CharField(max_length=16, verbose_name="电话", blank=True, null=True)
    ext_phone = models.CharField(max_length=16, verbose_name="分机", blank=True, null=True)
    birthday = models.DateField(verbose_name="生日", blank=True, null=True)
    is_lunar = models.SmallIntegerField(choices=is_lunar, verbose_name="生日农历or公历", default=0)
    native_place = models.CharField(max_length=64, verbose_name="籍贯", blank=True, null=True)
    delete_status = models.SmallIntegerField(choices=delete_status_choice, default=1, verbose_name='删除状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'linkman'
        verbose_name = '联系人'
        verbose_name_plural = '联系人'

    def __str__(self):
            return self.name

    _insert = ["supplier_id", "name", "gender", "job_title_id","age", "marriage", "mobile", "phone", "ext_phone",
               "birthday","is_lunar","native_place"]
    _update = ["supplier_id", "name", "gender", "age", "job_title_id", "marriage", "mobile", "phone", "ext_phone",
               "birthday","is_lunar","native_place"]


class GoodsAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    goods = models.ForeignKey('Goods', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='商品')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'goods_attach'
        verbose_name = '商品附件'
        verbose_name_plural = '商品附件'

    def __str__(self):
        return "商品附件:{0}".format(self.name)


class SupplierAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    supplier = models.ForeignKey('Supplier', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='供应商')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'supplier_attach'
        verbose_name = '供应商附件'
        verbose_name_plural = '供应商附件'

    def __str__(self):
        return "供应商附件:{0}".format(self.name)


class LinkmanAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    linkman = models.ForeignKey('Linkman', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='联系人')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'linkman_attach'
        verbose_name = '联系人附件'
        verbose_name_plural = '联系人附件'

    def __str__(self):
        return "联系人附件:{0}".format(self.name)


class LinkmanCard(models.Model):
    nid = models.AutoField(primary_key=True)
    linkman = models.ForeignKey("Linkman", to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='联系人')
    photo = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')

    class Meta:
        db_table = 'linkman_card'
        verbose_name = '联系人名片'
        verbose_name_plural = '联系人名片'

    def __str__(self):
        return "联系人名片:{0}".format(self.name)

    _update = ["photo","name"]


class LinkmanPhoto(models.Model):
    nid = models.AutoField(primary_key=True)
    linkman = models.ForeignKey('Linkman', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='联系人')
    photo = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')

    class Meta:
        db_table = 'linkman_photo'
        verbose_name = '联系人图片'
        verbose_name_plural = '联系人图片'

    def __str__(self):
        return "联系人图片:{0}".format(self.name)

    _update = ["photo","name"]



class SupplierLicence(models.Model):
    nid = models.AutoField(primary_key=True)
    supplier = models.ForeignKey('Supplier', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='供应商')
    photo = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')

    class Meta:
        db_table = 'supplier_licence'
        verbose_name = '供应商营业执照'
        verbose_name_plural = '供应商营业执照'

    def __str__(self):
        return "供应商营业执照:{0}".format(self.name)

    _update = ["photo","name"]


class SupplierPhoto(models.Model):
    nid = models.AutoField(primary_key=True)
    supplier = models.ForeignKey('Supplier', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='供应商')
    photo = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')

    class Meta:
        db_table = 'supplier_photo'
        verbose_name = '供应商公司图片'
        verbose_name_plural = '供应商公司图片'

    def __str__(self):
        return "供应商公司图片:{0}".format(self.name)

    _update = ["photo","name"]


class GoodsBarCode(models.Model):
    nid = models.AutoField(primary_key=True)
    goods = models.ForeignKey("Goods", to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='商品')
    photo = models.CharField(max_length=128, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')

    class Meta:
        db_table = 'goods_bar_code'
        verbose_name = '商品条码'
        verbose_name_plural = '商品条码'

    def __str__(self):
        return "商品条码:{0}".format(self.name)
    _update = ["photo","name"]


class GoodsPhoto(models.Model):
    nid = models.AutoField(primary_key=True)
    goods = models.ForeignKey("Goods", to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='商品')
    photo = models.CharField(max_length=128, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')

    class Meta:
        db_table = 'goods_photo'
        verbose_name = '商品图片'
        verbose_name_plural = '商品图片'

    def __str__(self):
        return "商品图片:{0}".format(self.name)

    _update = ["photo","name"]


class GoodsUnit(models.Model):
    nid = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=16,verbose_name="单位")

    class Meta:
        db_table = 'goods_unit'
        verbose_name = '商品单位'
        verbose_name_plural = '商品单位'

    def __str__(self):
        return self.caption

    _insert = ["caption"]
    _update = ["caption"]


class GoodsCategory(models.Model):
    nid = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=16,verbose_name="分类名称")
    parent = models.ForeignKey("self",to_field="nid",null=True,blank=True,on_delete=models.CASCADE, db_constraint=False,
                              verbose_name="上级分类")

    class Meta:
        db_table = 'goods_category'
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'

    def __str__(self):
        return self.caption


    _insert = ["caption","parent_id"]
    _update = ["caption","parent_id"]


class SupplierCategory(models.Model):
    nid = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=16,verbose_name="类别")

    class Meta:
        db_table = 'supplier_category'
        verbose_name = '供销商分类'
        verbose_name_plural = '供销商分类'

    def __str__(self):
        return self.caption

    _insert = ["caption"]
    _update = ["caption"]


class SupplierMemo(models.Model):
    nid = models.AutoField(primary_key=True)
    supplier = models.ForeignKey('Supplier', to_field="nid", on_delete=models.CASCADE, db_constraint=False,
                                 default=1, verbose_name='供应商')
    title = models.CharField(max_length=16,verbose_name="标题")
    detail = models.CharField(max_length=16,verbose_name="详细")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'supplier_memo'
        verbose_name = '供应商备忘'
        verbose_name_plural = '供应商备忘'

    def __str__(self):
        return self.title

    _insert = ["supplier_id","title",'detail']
    _update = ["supplier_id","title",'detail']


class MemoAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    memo = models.ForeignKey('SupplierMemo', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='供应商备忘')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'memo_attach'
        verbose_name = '备忘附件'
        verbose_name_plural = '备忘附件'

    def __str__(self):
        return "备忘附件:{0}".format(self.name)


class GoodsPrice(models.Model):
    delete_status_choice = ((0, '删除'), (1, '保留'))

    nid = models.IntegerField(primary_key=True)
    goods = models.ForeignKey('Goods', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='商品')
    unit = models.ForeignKey("GoodsUnit", to_field="nid", on_delete=models.CASCADE, verbose_name='单位',
                             db_constraint=False)
    amount = models.IntegerField(verbose_name="数量")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="单价")
    logistics = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="物流费用")
    logis_remark = models.CharField(verbose_name="物流备注",max_length=128, blank=True, null=True)
    supplier = models.ForeignKey('Supplier', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                                 verbose_name='供应商')
    linkman = models.ForeignKey('Linkman', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                                verbose_name='联系人')
    staff = models.ForeignKey(Staff, to_field='sid', on_delete=models.CASCADE, db_constraint=False,
                                    verbose_name='录入人')
    remark = models.CharField(verbose_name="备注",max_length=128, blank=True, null=True)
    date = models.DateField(verbose_name="报价日期")
    delete_status = models.SmallIntegerField(choices=delete_status_choice, default=1, verbose_name='删除状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'goods_price'
        verbose_name = '商品比价'
        verbose_name_plural = '商品比价'

    def __str__(self):
        return self.goods_id

    _insert = ["goods_id", "unit_id", 'amount','price', 'date','logistics','logis_remark',"supplier_id","linkman_id","staff_id","remark"]
    _update = ["goods_id", "unit_id", 'amount','price', 'date','logistics','logis_remark',"supplier_id","linkman_id","staff_id","remark"]


class PriceAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    price = models.ForeignKey("GoodsPrice", to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='供应来往')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'price_attach'
        verbose_name = '报价附件'
        verbose_name_plural = '报价附件'

    def __str__(self):
        return "报价附件:{0}".format(self.name)


class RetailSupplier(models.Model):
    nid = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=16, verbose_name="零食商家")

    class Meta:
        db_table = 'retail_supplier'
        verbose_name = '零售供应商'
        verbose_name_plural = '零售供应商'

    def __str__(self):
        return self.caption

    _insert = ["caption"]
    _update = ["caption"]


class PriceCompare(models.Model):
    delete_status_choice = ((0, '删除'), (1, '保留'))

    nid = models.AutoField(primary_key=True)
    goods = models.ForeignKey('Goods', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='商品')
    retail = models.ForeignKey('RetailSupplier', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                                 verbose_name='零售商')
    unit = models.ForeignKey("GoodsUnit", to_field="nid", on_delete=models.CASCADE, verbose_name='单位',
                             db_constraint=False)
    amount = models.IntegerField(verbose_name="数量")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="单价")
    date = models.DateField(verbose_name="比价日期")
    delete_status = models.SmallIntegerField(choices=delete_status_choice, default=1, verbose_name='删除状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'price_compare'
        verbose_name = '零售比价'
        verbose_name_plural = '零售比价'

    def __str__(self):
        return self.retail_id

    _insert = ["goods_id", "unit_id", 'amount', 'date','price',"retail_id"]
    _update = ["goods_id", "unit_id", 'amount', 'date', 'price',"retail_id"]


class Industry(models.Model):
    nid = models.AutoField(primary_key=True)
    industry = models.CharField(max_length=16,verbose_name="行业")

    class Meta:
        db_table = 'industry'
        verbose_name = '行业'
        verbose_name_plural = '行业'

    def __str__(self):
        return self.industry

    _insert = ["industry"]
    _update = ["industry"]


class Warehouse(models.Model):
    delete_status_choice = ((0, '删除'), (1, '保留'))
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32,verbose_name="仓库名称")
    town = models.ForeignKey(Town,on_delete=models.CASCADE, verbose_name='街道',
                             db_constraint=False,)
    address = models.CharField(max_length=128,verbose_name="详细地址")
    lng = models.DecimalField(max_digits=10, decimal_places=6, verbose_name="经度")
    lat = models.DecimalField(max_digits=10, decimal_places=6, verbose_name="纬度")
    delete_status = models.SmallIntegerField(choices=delete_status_choice, default=1, verbose_name='删除状态')

    class Meta:
        db_table = 'warehouse'
        verbose_name = '仓库'
        verbose_name_plural = "仓库"

    def __str__(self):
        return self.name

    _insert = ["name", "town_id", "address","lng","lat"]
    _update = ["name", "town_id", "address","lng","lat"]


class Inventory(models.Model):
    delete_status_choice = ((0, '删除'), (1, '保留'))

    nid = models.AutoField(primary_key=True)
    goods = models.ForeignKey("Goods",verbose_name="商品",on_delete=models.CASCADE,
                             db_constraint=False,)
    recorder = models.ForeignKey(Staff, verbose_name="录入员", on_delete=models.CASCADE, db_constraint=False)
    amount = models.IntegerField(verbose_name="入库数量")
    unit = models.ForeignKey("GoodsUnit", to_field="nid", on_delete=models.CASCADE, verbose_name='单位',
                             db_constraint=False)
    batch = models.IntegerField(verbose_name="入库批次")
    warehouse = models.ForeignKey("Warehouse",verbose_name="仓库", on_delete=models.CASCADE, db_constraint=False)
    location = models.ForeignKey("WareLocation",verbose_name="库位", on_delete=models.CASCADE, db_constraint=False)
    purchase = models.ForeignKey("Purchase", verbose_name="采购单",blank=True, null=True, on_delete=models.CASCADE, db_constraint=False)
    date = models.DateField(verbose_name="入库日期", blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')
    delete_status = models.SmallIntegerField(choices=delete_status_choice, default=1, verbose_name='删除状态')

    class Meta:
        db_table = 'inventory'
        verbose_name = '库存'
        verbose_name_plural = '库存'

    def __str__(self):
        return "库存：{0}".format(self.goods_id)

    _insert = ["warehouse_id", "goods_id",'recorder_id',"unit_id","location_id","amount","batch",'date']
    _update = ["warehouse_id", "goods_id",'recorder_id',"unit_id","location_id","amount","batch",'date']


class InventoryAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    inventory = models.ForeignKey('Inventory', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                                verbose_name='库存')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'inventory_attach'
        verbose_name = '入库凭证'
        verbose_name_plural = '入库凭证'

    def __str__(self):
        return "入库凭证:{0}".format(self.name)


class WareLocation(models.Model):
    nid = models.AutoField(primary_key=True)
    location = models.CharField(max_length=32, verbose_name="库位")
    warehouse = models.ForeignKey("Warehouse", to_field="nid", on_delete=models.CASCADE, verbose_name='所属仓库',
                               db_constraint=False)

    class Meta:
        db_table = 'ware_location'
        verbose_name = '库位'
        verbose_name_plural = '库位'

    def __str__(self):
        return self.location

    _insert = ["warehouse_id", "location"]
    _update = ["warehouse_id", "location"]


class Purchase(models.Model):
    delete_status_choice = ((0, '删除'), (1, '保留'))

    nid = models.AutoField(primary_key=True)
    goods = models.ForeignKey("Goods", verbose_name="采购商品", on_delete=models.CASCADE,
                              db_constraint=False, )
    supplier = models.ForeignKey("Supplier",verbose_name="供应商",on_delete=models.CASCADE,
                             db_constraint=False,)
    linkman = models.ForeignKey("SupplierContact", verbose_name="供应商联系人", on_delete=models.CASCADE,
                                    db_constraint=False)
    recorder = models.ForeignKey(Staff, verbose_name="录入员", on_delete=models.CASCADE, db_constraint=False)
    amount = models.IntegerField(verbose_name="采购数量")
    unit = models.ForeignKey("GoodsUnit", to_field="nid", on_delete=models.CASCADE, verbose_name='采购单位',
                             db_constraint=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="单价")
    total_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="单价")
    batch = models.IntegerField(verbose_name="采购批次")
    date = models.DateField(verbose_name="采购日期", blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')
    delete_status = models.SmallIntegerField(choices=delete_status_choice, default=1, verbose_name='删除状态')

    class Meta:
        db_table = 'purchase'
        verbose_name = '采购记录'
        verbose_name_plural = '采购记录'

    def __str__(self):
        return "采购：{0}".format(self.goods_id)

    _insert = ["goods_id","supplier_id", "linkman_id",'recorder_id',"unit_id","price","total_price","amount","batch",'date']
    _update = ["goods_id","supplier_id", "linkman_id",'recorder_id',"unit_id","price","total_price","amount","batch",'date']


class PurchaseAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    purchase = models.ForeignKey("Purchase", to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                                verbose_name='采购记录')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'purchase_attach'
        verbose_name = '采购凭证'
        verbose_name_plural = '采购凭证'

    def __str__(self):
        return "采购凭证:{0}".format(self.name)


class Repertory(models.Model):
    nid = models.AutoField(primary_key=True)
    goods = models.ForeignKey("Goods", to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                                 verbose_name='仓库库存')
    class Meta:
        db_table = 'repertory'
        verbose_name = '仓库库存'
        verbose_name_plural = '仓库库存'

    def __str__(self):
        return "仓库库存:{0}".format(self.goods)


class WastageGoods(models.Model):
    nid = models.AutoField(primary_key=True)
    goods = models.ForeignKey("Goods", verbose_name="损耗商品", on_delete=models.CASCADE,
                              db_constraint=False, )
    unit = models.ForeignKey("GoodsUnit", to_field="nid", on_delete=models.CASCADE, verbose_name='商品单位',
                             db_constraint=False)
    amount = models.IntegerField(verbose_name="损耗数量",blank=True, null=True)
    reason = models.TextField(verbose_name="损耗原因",blank=True, null=True)
    way = models.CharField(max_length=64,verbose_name="处置方式",blank=True, null=True)
    proposal = models.TextField(verbose_name="改进措施",blank=True, null=True)
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    date = models.DateField(verbose_name="日期", blank=True, null=True)
    recorder = models.ForeignKey(Staff,related_name="w_r", verbose_name="记录人", on_delete=models.CASCADE, db_constraint=False)
    solver = models.ManyToManyField(to=Staff,through="WastageSolver",through_fields=("wid", "sid"), verbose_name="处理人")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'wastage_goods'
        verbose_name = '损耗商品'
        verbose_name_plural = '损耗商品'

    def __str__(self):
        return "损耗商品:{0}".format(self.goods)

    _insert = ["goods_id", 'reason', "unit_id","recorder_id" ,"way", "amount","proposal", 'date']
    _update = ["goods_id", 'reason', "unit_id", "way","recorder_id" , "amount","proposal", 'date']


class WastageAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    wastage = models.ForeignKey("WastageGoods", to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                                 verbose_name='损耗记录')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'wastage_attach'
        verbose_name = '损耗附件'
        verbose_name_plural = '损耗附件'

    def __str__(self):
        return "损耗附件:{0}".format(self.name)


class WastageSolver(models.Model):
    nid = models.AutoField(primary_key=True)
    wid = models.ForeignKey('WastageGoods', to_field='nid', on_delete=models.CASCADE, db_constraint=False, verbose_name='损耗')
    sid = models.ForeignKey(Staff, to_field='sid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='处理人')

    class Meta:
        db_table = 'wastage_solver'
        unique_together = (('wid', 'sid'),)
        verbose_name = '损耗处理人'
        verbose_name_plural = '损耗处理人'

    def __str__(self):
        return '损耗处理人{0}'.format(self.sid)


class LinkmanTitle(models.Model):
    id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=32, blank=True, null=True, verbose_name='职称')

    class Meta:
        db_table = 'linkman_title'
        verbose_name = '联系人职称'
        verbose_name_plural = '联系人职称'

    def __str__(self):
        return self.job_title

    _insert = ["job_title"]
    _update = ["job_title"]
