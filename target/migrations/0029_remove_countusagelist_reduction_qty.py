# Generated by Django 3.1.5 on 2021-02-14 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0028_auto_20210214_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='countusagelist',
            name='reduction_qty',
        ),
    ]
