# Generated by Django 3.1.5 on 2021-01-07 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility_name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('sub_category', models.CharField(max_length=100)),
                ('facility_no', models.CharField(max_length=50)),
                ('dept_id', models.CharField(max_length=100)),
                ('account_number', models.CharField(max_length=100)),
                ('trans_code', models.CharField(max_length=100)),
                ('issue_date', models.DateTimeField()),
                ('imms', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('adjustment_number', models.CharField(max_length=100)),
                ('qty', models.IntegerField(default=0)),
                ('uom', models.CharField(max_length=50)),
                ('wt_avg_cost', models.FloatField()),
                ('ext_cost', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-ext_cost',),
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility_no', models.CharField(max_length=50)),
                ('facility_name', models.CharField(max_length=100)),
                ('po_date', models.DateTimeField()),
                ('po_no', models.CharField(max_length=100)),
                ('po_code', models.CharField(max_length=100)),
                ('po_submit_type', models.CharField(max_length=100)),
                ('vend_submit_type', models.CharField(max_length=100)),
                ('po_line_no', models.IntegerField()),
                ('imms', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('imms_vend_no', models.CharField(max_length=100)),
                ('vendor', models.CharField(max_length=100)),
                ('vendor_cat', models.CharField(max_length=100)),
                ('imms_contr_exp', models.CharField(max_length=100)),
                ('imms_contr_no', models.CharField(max_length=100)),
                ('mfr', models.CharField(max_length=100)),
                ('mfr_cat', models.CharField(max_length=100)),
                ('expense_acct_no', models.CharField(max_length=100)),
                ('expense_acct_desc', models.CharField(max_length=100)),
                ('dept_acct_no', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('po_qty', models.IntegerField(default=0)),
                ('po_price', models.FloatField()),
                ('po_ext', models.FloatField()),
                ('po_uom', models.CharField(max_length=100)),
                ('po_uom_mult', models.IntegerField()),
                ('low_uom_price', models.FloatField()),
            ],
            options={
                'ordering': ('-po_ext',),
            },
        ),
    ]
