# Generated by Django 3.1.5 on 2021-01-15 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0003_auto_20210114_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='countusagelist',
            name='ext_cost',
            field=models.FloatField(default=0),
        ),
    ]
