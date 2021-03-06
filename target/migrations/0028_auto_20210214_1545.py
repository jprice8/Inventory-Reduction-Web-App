# Generated by Django 3.1.5 on 2021-02-14 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0027_movementplan_isfinalized'),
    ]

    operations = [
        migrations.AddField(
            model_name='countusagelist',
            name='isHidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='movementplan',
            name='ship_qty',
            field=models.IntegerField(verbose_name='Quantity'),
        ),
    ]
