# Generated by Django 3.1.5 on 2021-02-23 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0030_auto_20210214_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movementplan',
            name='decision',
            field=models.CharField(choices=[('system', 'Ship to a facility within the system'), ('tenet', 'Ship to a Tenet facility'), ('sell', 'Sell to a third party vendor'), ('discard', 'Discard the item')], default='system', max_length=50),
        ),
    ]
