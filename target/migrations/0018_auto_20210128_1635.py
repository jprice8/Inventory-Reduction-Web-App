# Generated by Django 3.1.5 on 2021-01-28 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0017_auto_20210127_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='countusagelist',
            name='expense_account_desc',
            field=models.CharField(default='null', max_length=100),
        ),
        migrations.AddField(
            model_name='countusagelist',
            name='expense_account_no',
            field=models.IntegerField(default=0),
        ),
    ]