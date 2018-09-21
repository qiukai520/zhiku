from django.db import models

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
    goods = models.ForeignKey("Goods", to_field="nid", on_delete=models.CASCADE, verbose_name='主营商品',
                               db_constraint = False)
    introduce = models.CharField(max_length=512, verbose_name="简介", blank=True, null=True)
    website = models.CharField(max_length=64, verbose_name="网站", blank=True, null=True)
    phone = models.CharField(max_length=16, verbose_name="联系电话", blank=True, null=True)
    bank = models.CharField(max_length=512, verbose_name="开户银行", blank=True, null=True)
    bank_account = models.CharField(max_length=512, verbose_name="银行账户", blank=True, null=True)
    account_name = models.CharField(max_length=512, verbose_name="账户名", blank=True, null=True)
    country = models.ForeignKey("Country", to_field="nid", on_delete=models.CASCADE, verbose_name='县(区',
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

    _insert = [ "category_id","company", "industry_id", "employees","goods_id","introduce",'website',"remark","address",
                "country_id","account_name","bank_account","bank","phone"]
    _update = ["category_id", "company", "industry_id", "employees", "goods_id", "introduce", 'website', "remark", "address",
               "country_id", "account_name", "bank_account", "bank", "phone"]


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
    standard = models.CharField(max_length=32,verbose_name='商品规格', blank=True, null=True)
    start_month = models.SmallIntegerField(blank=True, null=True, verbose_name='起始产期(月份)',)
    end_month = models.SmallIntegerField(blank=True, null=True, verbose_name='结束期(月份)')
    country = models.ForeignKey("Country", to_field="nid", on_delete=models.CASCADE, verbose_name='县(区',
                                db_constraint=False)
    delete_status = models.SmallIntegerField(choices=delete_status_choice, default=1, verbose_name='删除状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'goods'
        verbose_name = '商品'
        verbose_name_plural = '商品'

    def __str__(self):
        return self.name
    _insert=["category_id","name","description","unit_id","code","standard","start_month","end_month","country_id"]
    _update=["category_id","name","description","unit_id","code","standard","start_month","end_month","country_id"]


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

    _insert = ["supplier_id", "name", "gender", "age", "marriage", "mobile", "phone", "ext_phone",
               "birthday","is_lunar","native_place"]
    _update = ["supplier_id", "name", "gender", "age", "marriage", "mobile", "phone", "ext_phone",
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
                            verbose_name='商品')
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
                            verbose_name='商品')
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
    caption = models.CharField(max_length=16,verbose_name="商品分类")

    class Meta:
        db_table = 'goods_category'
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'

    def __str__(self):
        return self.caption


    _insert = ["caption"]
    _update = ["caption"]


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


class Nation(models.Model):
    nid = models.AutoField(primary_key=True)
    nation = models.CharField(max_length=16, verbose_name="国家")

    class Meta:
        db_table = 'nation'
        verbose_name = '国家'
        verbose_name_plural = '国家'

    def __str__(self):
        return self.nation

    _insert = ["nation"]
    _update = ["nation"]


class Province(models.Model):
    nid = models.AutoField(primary_key=True)
    province = models.CharField(max_length=16, verbose_name="省份")
    nation = models.ForeignKey(Nation, to_field="nid", on_delete=models.CASCADE, verbose_name='国家',
                                 db_constraint=False)

    class Meta:
        db_table = 'province'
        verbose_name = '省份'
        verbose_name_plural = '省份'

    def __str__(self):
        return self.province

    _insert = ["province", "nation_id"]
    _update = ["province", "nation_id"]


class City(models.Model):
    nid = models.AutoField(primary_key=True)
    city = models.CharField(max_length=16, verbose_name="城市")
    province = models.ForeignKey(Province, to_field="nid", on_delete=models.CASCADE, verbose_name='省份',
                               db_constraint=False)

    class Meta:
        db_table = 'city'
        verbose_name = '城市'
        verbose_name_plural = '城市'

    def __str__(self):
        return self.city

    _insert = ["province_id", "city"]
    _update = ["province_id", "city"]


class Country(models.Model):
    nid = models.AutoField(primary_key=True)
    country = models.CharField(max_length=16, verbose_name="县(区)")
    city = models.ForeignKey(City, to_field="nid", on_delete=models.CASCADE, verbose_name='城市',
                             db_constraint=False,)

    class Meta:
        db_table = 'country'
        verbose_name = '县(区)'
        verbose_name_plural = '县(区)'

    def __str__(self):
        return self.country

    _insert = ["city_id", "country"]
    _update = ["city_id", "country"]


