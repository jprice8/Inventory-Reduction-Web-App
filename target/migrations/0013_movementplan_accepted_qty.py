# Generated by Django 3.1.5 on 2021-01-23 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0012_auto_20210121_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='movementplan',
            name='accepted_qty',
            field=models.IntegerField(default=0),
        ),
    ]
