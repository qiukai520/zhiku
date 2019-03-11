from rbac.models import Role,User as UserProfile


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
    birthday = models.DateField(verbose_name="生日", blank=True, null=True)
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