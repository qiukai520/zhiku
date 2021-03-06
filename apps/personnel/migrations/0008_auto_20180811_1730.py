# Generated by Django 2.0 on 2018-08-11 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0007_jobtitle_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='job_title',
            field=models.ForeignKey(db_constraint=False, default=1, on_delete=django.db.models.deletion.CASCADE, to='personnel.JobTitle', verbose_name='职称'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='company',
            field=models.ForeignKey(db_constraint=False, default=1, on_delete=django.db.models.deletion.CASCADE, to='personnel.Company', verbose_name='所在公司'),
        ),
    ]
