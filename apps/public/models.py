from django.db import models

# Create your models here.


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
    code = models.IntegerField(verbose_name="编码")
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
    code = models.IntegerField(verbose_name="编码")
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
    code = models.IntegerField(verbose_name="编码")
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


class Town(models.Model):
    nid = models.AutoField(primary_key=True)
    code = models.IntegerField(verbose_name="编码")
    town = models.CharField(max_length=16, verbose_name="街道")
    country = models.ForeignKey(Country, to_field="nid", on_delete=models.CASCADE, verbose_name='县区',
                             db_constraint=False,)

    class Meta:
        db_table = 'town'
        verbose_name = '街道'
        verbose_name_plural = "街道"

    def __str__(self):
        return self.town

    _insert = ["town", "country_id"]
    _update = ["town", "country_id"]
