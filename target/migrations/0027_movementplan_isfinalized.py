# Generated by Django 3.1.5 on 2021-02-14 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0026_auto_20210212_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='movementplan',
            name='isFinalized',
            field=models.BooleanField(default=False),
        ),
    ]
