# Generated by Django 3.1.5 on 2021-01-14 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_facility'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='facility_name',
            field=models.CharField(default='939', max_length=100),
        ),
    ]
