# Generated by Django 3.1.5 on 2021-01-18 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0008_auto_20210117_1858'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='countusagelist',
            name='listing',
        ),
        migrations.AddField(
            model_name='countusagelist',
            name='isTarget',
            field=models.BooleanField(default=False),
        ),
    ]
