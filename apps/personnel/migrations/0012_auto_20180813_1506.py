# Generated by Django 2.0 on 2018-08-13 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0011_stafflifephoto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staff',
            old_name='sex',
            new_name='gender',
        ),
    ]
