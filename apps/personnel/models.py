from django.db import models
from rbac.models import Role,User as UserProfile


# Create your models here.


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=32, blank=True, null=True, verbose_name='部门')

    class Meta:
        db_table = 'department'
        verbose_name = '部门'
        verbose_name_plural = '部门'

    def __str__(self):
        return self.department

    _insert = ["department"]
    _update = ["department"]


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.CharField(max_length=32, blank=True, null=True, verbose_name='公司')

    class Meta:
        db_table = 'company'
        verbose_name = '公司'
        verbose_name_plural = '公司'

    def __str__(self):
        return self.company

    _insert = ["company"]
    _update = ["company"]


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.CharField(max_length=32, blank=True, null=True, verbose_name='所在项目')

    class Meta:
        db_table = 'project'
        verbose_name = '所在项目'
        verbose_name_plural = '所在项目'

    def __str__(self):
        return self.project

    _insert = ["project"]
    _update = ["project"]


class Select_Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True, verbose_name='选择项目')

    class Meta:
        db_table = 's_project'
        verbose_name = '选择项目'
        verbose_name_plural = '选择项目'

    def __str__(self):
        return self.name

    _insert = ["s_project"]
    _update = ["s_project"]


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True, verbose_name='用品')

    class Meta:
        db_table = 'article'
        verbose_name = '用品'
        verbose_name_plural = '用品'

    def __str__(self):
        return self.name

    _insert = ["article"]
    _update = ["article"]

class ReasonsPeople(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, verbose_name='工作交接人')

    class Meta:
        db_table = 'reasons_people'
        verbose_name = '工作交接人'
        verbose_name_plural = '工作交接人'

    def __str__(self):
        return self.name

    _insert = ["reasons_people"]
    _update = ["reasons_people"]

class ReasonsCause(models.Model):
    id = models.AutoField(primary_key=True)
    cause = models.CharField(max_length=32, blank=True, null=True, verbose_name='原因')

    class Meta:
        db_table = 'reasons_cause'
        verbose_name = '原因'
        verbose_name_plural = '原因'

    def __str__(self):
        return self.cause

    _insert = ["cause"]
    _update = ["cause"]

class JobRank(models.Model):
    id = models.AutoField(primary_key=True)
    rank = models.CharField(max_length=32, blank=True, null=True, verbose_name='职级')

    class Meta:
        db_table = 'job_rank'
        verbose_name = '职级'
        verbose_name_plural = '职级'

    def __str__(self):
        return self.rank

    _insert = ["rank"]
    _update = ["rank"]


class JobTitle(models.Model):
    id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=32, blank=True, null=True, verbose_name='职称')
    department = models.ForeignKey('Department', to_field="id", on_delete=models.CASCADE, db_constraint=False,
                                   default=1, verbose_name='所属部门')

    class Meta:
        db_table = 'job_title'
        verbose_name = '职称'
        verbose_name_plural = '职称'

    def __str__(self):
        return self.job_title

    _insert = ["job_title"]
    _update = ["job_title"]


class Staff(models.Model):
    gender_choice = ((0, "男"), (1, "女"))
    is_lunar = ((0, "公历"), (1, "农历"))
    delete_status_choice = ((0, '离职'), (1, '在职'))

    sid = models.AutoField(primary_key=True)
    job_number = models.CharField(max_length=32, verbose_name='工号')
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, db_constraint=False,verbose_name="用户", blank=True, null=True)
    name = models.CharField(max_length=32, verbose_name='员工姓名')
    gender = models.SmallIntegerField(choices=gender_choice, verbose_name="性别", default=0)
    phone = models.CharField(max_length=11, verbose_name="手机号码", blank=True, null=True)
    email = models.EmailField(verbose_name="邮箱", blank=True, null=True)
    company = models.ForeignKey('Company', to_field="id", on_delete=models.CASCADE, db_constraint=False,
                                   default=1, verbose_name='所在公司')
    project = models.ForeignKey('Project', to_field="id", on_delete=models.CASCADE, db_constraint=False,
                                   default=1, verbose_name='所在项目')
    department = models.ForeignKey('Department', to_field="id", on_delete=models.CASCADE, db_constraint=False,
                                   default=1, verbose_name='所属部门')
    job_rank = models.ForeignKey('JobRank', to_field="id", on_delete=models.CASCADE, db_constraint=False,
                                   default=1, verbose_name='职级', blank=True, null=True)
    job_title = models.ForeignKey('JobTitle', to_field="id", on_delete=models.CASCADE, db_constraint=False,
                                 default=1, verbose_name='职称', blank=True, null=True)
    birthday = models.DateField(verbose_name="生日", auto_now_add=False, blank=True, null=True)
    is_lunar = models.SmallIntegerField(choices=is_lunar, verbose_name="生日农历or公历", default=0)
    hire_day = models.DateField(verbose_name="入职日期", blank=True, null=True)
    native_place = models.CharField(max_length=64, verbose_name="籍贯", blank=True, null=True)
    nationality = models.CharField(max_length=32, verbose_name='民族', blank=True, null=True)
    family_address = models.CharField(max_length=128, verbose_name="家庭住址", blank=True, null=True)
    current_address = models.CharField(max_length=128, verbose_name="现住地址",blank=True, null=True)
    education = models.CharField(max_length=32, verbose_name='学历', blank=True, null=True)
    id_card = models.CharField(max_length=18, verbose_name="身份证号", blank=True, null=True)
    roles = models.ManyToManyField(Role, verbose_name="角色", blank=True)
    bank = models.CharField(max_length=32, verbose_name="开户银行",blank=True, null=True)
    bank_account = models.CharField(max_length=21, verbose_name="银行账号", blank=True, null=True)
    account_name = models.CharField(max_length=21, verbose_name="开户人", blank=True, null=True)
    contact_phone = models.CharField(max_length=11, verbose_name="紧急联系人号码", blank=True, null=True)
    contact_man = models.CharField(max_length=32, verbose_name="紧急联系人", blank=True, null=True)
    contact_relation = models.CharField(max_length=16, verbose_name='紧急联系人关系', blank=True, null=True)
    recruit_channel = models.CharField(max_length=16, verbose_name='招聘渠道', blank=True, null=True)
    referrer = models.CharField(max_length=16, verbose_name='引荐人', blank=True, null=True)
    remark = models.CharField(max_length=512, verbose_name="备注", blank=True, null=True)
    delete_status = models.SmallIntegerField(choices=delete_status_choice, default=1, verbose_name='在职状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'staff'
        verbose_name = '员工'
        verbose_name_plural = '员工'

    def __str__(self):
            return self.name

    _insert = ["job_number", "name", "gender","phone","email", "company_id", "project_id", "department_id",
                 "birthday", "is_lunar","job_rank_id", "job_title_id","hire_day","native_place", "nationality",
               "family_address","referrer","current_address", "education","id_card","bank","bank_account", "account_name",
               "contact_phone","contact_man","contact_relation", "recruit_channel", "remark"]

    _update = ["sid","job_number", "name", "gender", "phone", "email", "company_id", "project_id", "department_id",
               "birthday", "is_lunar", "job_rank_id", "job_title_id", "hire_day", "native_place", "nationality",
               "family_address","referrer","current_address", "education", "id_card", "bank", "bank_account", "account_name",
               "contact_phone","contact_man", "contact_relation", "recruit_channel", "remark"]

class StaffAttach(models.Model):
    said = models.AutoField(primary_key=True)
    sid = models.ForeignKey('Staff', to_field='sid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='员工')
    attachment = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=512, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'staff_attach'
        verbose_name = '员工附件'
        verbose_name_plural = '员工附件'

    def __str__(self):
        return "员工附件:{0}".format(self.sid)


class StaffLifePhoto(models.Model):
    id = models.AutoField(primary_key=True)
    sid = models.ForeignKey('Staff', to_field='sid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='员工')
    life_photo = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')

    class Meta:
        db_table = 'staff_life_photo'
        verbose_name = '员工生活照'
        verbose_name_plural = '员工生活照'

    def __str__(self):
        return "员工生活照:{0}".format(self.sid)

    _update = ["life_photo", "name"]


# 增加就职表现
class Performanceyg(models.Model):
    nid = models.AutoField(primary_key=True)
    sid = models.ForeignKey('Staff', to_field='sid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='员工')
    select_project_id = models.ForeignKey('Select_Project', to_field="id", on_delete=models.CASCADE,
                                          db_constraint=False,
                                          default=1, verbose_name='选择项目')
    content = models.TextField(max_length=512, verbose_name="内容明细", blank=True, null=True)
    effective_time = models.DateTimeField( verbose_name='生效时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')
    operator_id = models.CharField(max_length=12, verbose_name='操作人')

    class Meta:
        db_table = 'performanceyg'
        verbose_name = '就职表现'
        verbose_name_plural = '就职表现'

    def __str__(self):
        return self.sid

    _insert = ["sid_id", "select_project_id_id", "content", "effective_time", "operator_id"]

    _update = ["sid_id", "select_project_id_id", "content", "effective_time", "operator_id"]


# 就职表现附件
class PerforygmanceAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    sid = models.ForeignKey('Performanceyg', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='就职附件')
    attachment = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'perforygmance_attach'
        verbose_name = '就职附件'
        verbose_name_plural = '就职附件'

    def __str__(self):
        return "就职附件:{0}".format(self.sid)

    _update = ["nid", "attachment", "name", "description"]


# 劳动合同
class LaborContract(models.Model):
    nid = models.AutoField(primary_key=True)
    sid = models.ForeignKey('Staff', to_field='sid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='员工')
    remark = models.TextField(max_length=512, verbose_name="备注", blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='开始时间')
    end_time = models.DateTimeField(auto_now_add=False, verbose_name='结束时间')

    class Meta:
        db_table = 'labor_contract'
        verbose_name = '劳动合同'
        verbose_name_plural = '劳动合同'

    def __str__(self):
        return self.remark

    _insert = ["sid_id", "remark", "create_time", "end_time"]

    _update = ["nid", "sid_id", "remark", "create_time", "end_time"]


# 合同劳动附件附件
class Labor_Contract_Attach(models.Model):
    nid = models.AutoField(primary_key=True)
    sid = models.ForeignKey('LaborContract', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='合同附件')
    attachment = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'labor_contract_attach'
        verbose_name = '合同附件'
        verbose_name_plural = '合同附件'

    def __str__(self):
        return "合同附件:{0}".format(self.sid)

    _update = ["attachment", "name", "description"]


# 离职原因
class ReasonsLeave(models.Model):
    nid = models.AutoField(primary_key=True)
    sid = models.ForeignKey('Staff', to_field='sid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='员工')
    reasons_cause = models.ForeignKey('ReasonsCause', to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name='原因')
    reasons = models.TextField(max_length=512, verbose_name="离职原因", blank=True, null=True)
    reasons_time = models.DateTimeField(auto_now_add=True, verbose_name='工资计算截止日期')
    reasons_bool1 = models.BooleanField(default=True, verbose_name="停用账号")
    reasons_bool2 = models.BooleanField(default=True, verbose_name="停买社保")
    reasons_people = models.ForeignKey('ReasonsPeople', to_field='id', on_delete=models.CASCADE, db_constraint=False, verbose_name='工作交接人')
    reasons_time1 = models.DateTimeField(auto_now_add=True, verbose_name='离岗日期')

    class Meta:
        db_table = 'reasonsleave'
        verbose_name = '离职原因'
        verbose_name_plural = '离职原因'

    def __str__(self):
        return self.reasons

    _insert = ["sid_id", "reasons_cause_id", "reasons", "reasons_time", "reasons_bool1", "reasons_bool2", "reasons_people_id", "reasons_time1"]

    _update = ["nid", "sid_id", "reasons_cause_id", "reasons", "reasons_time", "reasons_bool1", "reasons_bool2", "reasons_people_id", "reasons_time1"]


# 离职原因附件附件
class Reasonsleave_Attach(models.Model):
    nid = models.AutoField(primary_key=True)
    sid = models.ForeignKey('ReasonsLeave', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='离职附件')
    attachment = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'reasons_attach'
        verbose_name = '离职附件'
        verbose_name_plural = '离职附件'

    def __str__(self):
        return "离职附件:{0}".format(self.sid)

    _update = ["attachment", "name", "description"]


# 社保管理
class SocialSecurity(models.Model):
    nid = models.AutoField(primary_key=True)
    sid = models.ForeignKey('Staff', to_field='sid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='员工')
    s_id = models.CharField(max_length=80, verbose_name="社保卡号", blank=True, null=True)
    s_money = models.DecimalField(max_digits=20, decimal_places=10, verbose_name="购买金额", blank=True, null=True)
    s_time = models.DateTimeField(auto_now_add=True, verbose_name='起始时间')
    s_remark = models.TextField(max_length=512, verbose_name="备注", blank=True, null=True)

    class Meta:
        db_table = 'social_security'
        verbose_name = '社保管理'
        verbose_name_plural = '社保管理'

    def __str__(self):
        return self.s_id

    _insert = ['sid_id', "s_id", 's_money', 's_time', 's_remark']

    _update = ['id', "sid_id", "s_id", 's_money', 's_time', 's_remark']


class Social_Attach(models.Model):
    nid = models.AutoField(primary_key=True)
    sid = models.ForeignKey('SocialSecurity', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='社保管理附件')
    attachment = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'social_attach'
        verbose_name = '社保附件'
        verbose_name_plural = '社保附件'

    def __str__(self):
        return "社保附件:{0}".format(self.sid)

    _update = ["attachment", "name", "description"]


# 用品领用
class Supplies(models.Model):
    nid = models.AutoField(primary_key=True)
    sid = models.ForeignKey('Staff', to_field='sid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='员工')
    supplies_id = models.ForeignKey('Article', to_field='id', on_delete=models.CASCADE, db_constraint=False,
                                    verbose_name='用品')
    supplies_time = models.DateTimeField(auto_now_add=True, verbose_name='领用日')
    supplies_remark = models.TextField(max_length=512, verbose_name="备注", blank=True, null=True)

    class Meta:
        db_table = 'supplies'
        verbose_name = '用品领用'
        verbose_name_plural = '用品领用'

    def __str__(self):
        return self.sid_id

    _insert = ['sid_id', 'supplies_id_id', 'supplies_time', 'supplies_remark']

    _update = ['id', 'sid_id', 'supplies_id_id', 'supplies_time', 'supplies_remark']


# 用品领用附件
class Supplies_Attach(models.Model):
    nid = models.AutoField(primary_key=True)
    sid = models.ForeignKey('Supplies', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='用品领用附件')
    attachment = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'supplies_attach'
        verbose_name = '用品领用附件'
        verbose_name_plural = '用品领用附件'

    def __str__(self):
        return "用品领用附件:{0}".format(self.sid)

    _update = ["attachment", "name", "description"]


# 用品归还
class Supplies_Return(models.Model):
    nid = models.AutoField(primary_key=True)
    sid = models.ForeignKey('Staff', to_field='sid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='员工')
    supplies_id = models.ForeignKey('Article', to_field='id', on_delete=models.CASCADE, db_constraint=False,
                                    verbose_name='用品')
    remark = models.TextField(max_length=512, verbose_name='归还备注', blank=True, null=True)
    return_time = models.DateTimeField(auto_now_add=True, verbose_name='归还时间')

    class Meta:
        db_table = 'supplies_return'
        verbose_name = '用品归还'
        verbose_name_plural = '用品归还'

    def __str__(self):
        return self.sid_id

    _insert = ['sid_id', 'supplies_id_id', 'remark', 'return_time']

    _update = ['id', 'sid_id', 'supplies_id_id', 'remark', 'return_time']

# 用品归还附件
class Supplies_Return_Attach(models.Model):
    nid = models.AutoField(primary_key=True)
    sid = models.ForeignKey('Supplies_Return', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='用品归还附件')
    attachment = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'supplies_return_attach'
        verbose_name = '用品领用附件'
        verbose_name_plural = '用品领用附件'

    def __str__(self):
        return "用品领用附件:{0}".format(self.sid)

    _update = ["attachment", "name", "description"]
