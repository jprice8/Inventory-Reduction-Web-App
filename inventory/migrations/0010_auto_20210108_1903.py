# Generated by Django 3.1.5 on 2021-01-09 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_delete_countusagelist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invcount',
            name='cost',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='invcount',
            name='ext',
            field=models.FloatField(default=0),
        ),
    ]
