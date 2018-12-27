# Generated by Django 2.0 on 2018-08-13 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0010_staff_job_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffLifePhoto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('life_photo', models.CharField(blank=True, max_length=512, null=True, verbose_name='路径')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='名称')),
                ('sid', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='personnel.Staff', verbose_name='员工')),
            ],
            options={
                'verbose_name': '员工生活照',
                'verbose_name_plural': '员工生活照',
                'db_table': 'staff_life_photo',
            },
        ),
    ]