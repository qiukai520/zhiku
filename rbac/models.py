from django.db import models

# Create your models here
# Create your models here.


class Menu(models.Model):
    """
    菜单组
    """
    title = models.CharField(max_length=32)

    class Meta:
        db_table = 'menu'
        verbose_name = '菜单组'
        verbose_name_plural = '菜单组'

    def __str__(self):
        return self.title


class Group(models.Model):
    """
    权限组
    """
    caption = models.CharField(max_length=32, verbose_name="组名")
    menu = models.ForeignKey(verbose_name="所属菜单",to="Menu",on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'group'
        verbose_name = '权限组'
        verbose_name_plural = '权限组'

    def __str__(self):
        return self.caption


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name="标题", max_length=32)
    url = models.CharField(max_length=64, verbose_name="含正则的url")
    menu_gp = models.ForeignKey(verbose_name="组内菜单", on_delete=models.CASCADE,to="Permission", null=True, blank=True, related_name="x1")
    code = models.CharField(verbose_name="代码", max_length=16)
    group = models.ForeignKey(verbose_name="所属组", to="Group",on_delete=models.CASCADE)

    class Meta:
        db_table = 'permission'
        verbose_name = '权限表'
        verbose_name_plural = "权限表"

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色表
    """
    title = models.CharField(max_length=32)
    permission = models.ManyToManyField(verbose_name="具有的所有的权限", to="Permission", blank=True)

    class Meta:
        db_table = 'role'
        verbose_name = '角色表'
        verbose_name_plural = "角色表"

    def __str__(self):
        return self.title


# class User(models.Model):
#     """
#     用户表
#     """
#     username = models.CharField(verbose_name="用户表", max_length=32)
#     password = models.CharField(verbose_name="密码", max_length=64)
#     email = models.CharField(verbose_name="邮箱", max_length=32)
#     roles = models.ManyToManyField(verbose_name="具有的所有的角色", to="Role", blank=True)
#
#     class Meta:
#         verbose_name_plural = "用户表"
#
#     def __str__(self):
#         return self.username