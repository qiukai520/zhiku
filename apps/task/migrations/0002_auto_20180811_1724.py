# Generated by Django 2.0 on 2018-08-11 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskassignattach',
            name='attach',
        ),
        migrations.RemoveField(
            model_name='taskattachment',
            name='attach',
        ),
        migrations.RemoveField(
            model_name='tasksubmitattachment',
            name='attach',
        ),
        migrations.AddField(
            model_name='taskassignattach',
            name='attachment',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='附件路径'),
        ),
        migrations.AddField(
            model_name='taskattachment',
            name='attachment',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='附件路径'),
        ),
        migrations.AddField(
            model_name='tasksubmitattachment',
            name='attachment',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='附件路径'),
        ),
    ]
