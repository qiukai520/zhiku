import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password,check_password
from django.db import models
# from sfa.models import SoftDeletableModel
# Create your models here


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
    menu_gp = models.ForeignKey(verbose_name="组内菜单", on_delete=models.CASCADE, to="Permission", null=True, blank=True, related_name="x1")
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


# class UserProfile(models.Model):
#     """
#     用户表
#     """
#     username=models.CharField(max_length=128,verbose_name="用户名")
#     password=models.CharField(max_length=128,verbose_name="密码")
#     is_active=models.BooleanField(verbose_name="激活状态",default=1)
#     is_superuser=models.BooleanField(verbose_name="用户角色",default=0)
#     roles = models.ManyToManyField(Role,verbose_name="具有的所有的角色",  through='User2Role',
#
#                                                 through_fields=('user', 'role'),)
#     create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
#
#     class Meta:
#         db_table = 'user_profile'
#         verbose_name = '用户表'
#         verbose_name_plural = '用户表'
#
#     def __str__(self):
#         return self.username
#
#     def save(self,*args, **kwargs):
#         self.password = make_password(self.password)
#         super(UserProfile, self).save(*args, **kwargs)
#
#     def set_password(self, raw_password):
#         self.password = make_password(raw_password)
#         self._password = raw_password
#
#     def check_password(self, raw_password):
#         """
#         Return a boolean of whether the raw_password was correct. Handles
#         hashing formats behind the scenes.
#         """
#
#         def setter(raw_password):
#             self.set_password(raw_password)
#             # Password hash upgrades shouldn't be considered password changes.
#             self._password = None
#             self.save(update_fields=["password"])
#
#         return check_password(raw_password, self.password, setter)


class User(AbstractUser):
    """
    用户表
    """
    # roles = models.ManyToManyField(Role,verbose_name="前台角色",  through='User2Role',
    #
    #                                             through_fields=('user', 'role'),)
    phone = models.CharField(max_length=11, verbose_name="手机号码")


    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'
        verbose_name = '用户表'
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.username

    # def save(self,*args, **kwargs):
    #     self.password = make_password(self.password)
    #     print("save",self.password)
    #     super(User, self).save(*args, **kwargs)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)


class UserLog(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name='操作用户')
    remote_ip = models.GenericIPAddressField(verbose_name='操作用户IP')
    content = models.CharField(max_length=100, verbose_name='操作内容')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')

    class Meta:
        db_table = 'users_log'
        verbose_name = '用户管理操作记录表'
        verbose_name_plural = '用户管理操作记录表'
