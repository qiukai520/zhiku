from django.db import models

# Create your models here.


class Supplier(models.Model):
    nid = models.AutoField(primary_key=True)
    category = models.ForeignKey("SupplierCategory", to_field="nid", on_delete=models.CASCADE, verbose_name='分类',
                               db_constraint=False)
    company = models.CharField(max_length=64,verbose_name="公司名称")
    industry = models.ForeignKey("Industry", to_field="nid", on_delete=models.CASCADE, verbose_name='行业',
                               db_constraint=False)
    employees = models.IntegerField(verbose_name='公司人数')
    goods = models.ForeignKey("Goods", to_field="nid", on_delete=models.CASCADE, verbose_name='主营商品',
                               db_constraint=False)
    introduce = models.CharField(max_length=512, verbose_name="简介")
    website = models.CharField(max_length=64, verbose_name="网站")
    phone = models.CharField(max_length=16, verbose_name="电话")
    bank = models.CharField(max_length=512,verbose_name="开户银行")
    bank_account = models.CharField(max_length=512,verbose_name="银行账户")
    account_name = models.CharField(max_length=512,verbose_name="账户名")
    country = models.ForeignKey(Country, to_field="nid", on_delete=models.CASCADE, verbose_name='县(区',
                               db_constraint=False)
    address = models.CharField(max_length=64, verbose_name="地址")
    remark = models.CharField(max_length=512, verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')


    class Meta:
        db_table = 'supplier'
        verbose_name = '供应商'
        verbose_name_plural = '供应商'

    def __str__(self):
        return self.company



class Goods(models.Model):
    nid = models.AutoField(primary_key=True)
    category = models.ForeignKey("GoodsCategory", to_field="nid", on_delete=models.CASCADE, verbose_name='商品分类',
                               db_constraint=False)
    name = models.CharField(max_length=64,verbose_name="商品名称")
    description = models.CharField(max_length=256,verbose_name="描述")

    unit = models.ForeignKey("GoodsUnit", to_field="nid", on_delete=models.CASCADE, verbose_name='商品单位',
                               db_constraint=False)
    standard = models.IntegerField(verbose_name='商品规格')
    start_time = models.DateTimeField(blank=True, null=True, verbose_name='起始产期')
    deadline = models.DateTimeField(blank=True, null=True, verbose_name='结束产期')
    country = models.ForeignKey(Country, to_field="nid", on_delete=models.CASCADE, verbose_name='县(区',
                                db_constraint=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')


    class Meta:
        db_table = 'supplier'
        verbose_name = '供应商'
        verbose_name_plural = '供应商'

    def __str__(self):
        return self.company


class GoodsUnit(models.Model):
    nid = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=16,verbose_name="单位")

    class Meta:
        db_table = 'goods_unit'
        verbose_name = '商品单位'
        verbose_name_plural = '商品单位'

    def __str__(self):
        return self.category



class GoodsCategory(models.Model):
    nid = models.AutoField(primary_key=True)
    category = models.CharField(max_length=16,verbose_name="类别")

    class Meta:
        db_table = 'goods_category'
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'

    def __str__(self):
        return self.category


class SupplierCategory(models.Model):
    nid = models.AutoField(primary_key=True)
    category = models.CharField(max_length=16,verbose_name="类别")

    class Meta:
        db_table = 'supplier_category'
        verbose_name = '供销商分类'
        verbose_name_plural = '供销商分类'

    def __str__(self):
        return self.category


class Industry(models.Model):
    nid = models.AutoField(primary_key=True)
    industry = models.CharField(max_length=16,verbose_name="行业")

    class Meta:
        db_table = 'industry'
        verbose_name = '行业'
        verbose_name_plural = '行业'

    def __str__(self):
        return self.industry


class Nation(models.Model):
    nid = models.AutoField(primary_key=True)
    nation = models.CharField(max_length=16,verbose_name="国家")

    class Meta:
        db_table = 'nation'
        verbose_name = '国家'
        verbose_name_plural = '国家'

    def __str__(self):
        return self.nation


class Province(models.Model):
    nid = models.AutoField(primary_key=True)
    province = models.CharField(max_length=16,verbose_name="省份")

    class Meta:
        db_table = 'province'
        verbose_name = '省份'
        verbose_name_plural = '省份'

    def __str__(self):
        return self.province


class City(models.Model):
    nid = models.AutoField(primary_key=True)
    city=models.CharField(max_length=16,verbose_name="城市")
    province = models.ForeignKey(Province, to_field="nid", on_delete=models.CASCADE, verbose_name='省份',
                               db_constraint=False)

    class Meta:
        db_table = 'city'
        verbose_name = '城市'
        verbose_name_plural = '城市'

    def __str__(self):
        return self.city


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
        return self.city
