# Generated by Django 3.1.5 on 2021-01-08 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20210107_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountUsageList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.DateTimeField()),
                ('fac', models.CharField(max_length=50)),
                ('imms', models.CharField(max_length=50)),
                ('count_qty', models.IntegerField()),
                ('issue_qty', models.IntegerField()),
                ('po_qty', models.IntegerField()),
                ('facility_name', models.CharField(max_length=50)),
                ('mfr', models.CharField(max_length=100)),
                ('mfr_cat_no', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('imms_create_date', models.DateTimeField()),
                ('vendor', models.CharField(max_length=100)),
                ('vend_cat_no', models.CharField(max_length=100)),
                ('default_uom', models.CharField(max_length=10)),
                ('default_uom_conv', models.IntegerField()),
                ('default_uom_price', models.FloatField()),
                ('luom', models.CharField(max_length=10)),
                ('luom_conv', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Issue',
        ),
        migrations.DeleteModel(
            name='PurchaseOrder',
        ),
    ]
