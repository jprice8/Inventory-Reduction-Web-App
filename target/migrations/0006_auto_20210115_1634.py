# Generated by Django 3.1.5 on 2021-01-15 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0005_auto_20210115_1612'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='countusagelist',
            options={'ordering': ('-ext_cost',)},
        ),
        migrations.AddField(
            model_name='countusagelist',
            name='reduction_qty',
            field=models.IntegerField(default=0),
        ),
    ]
