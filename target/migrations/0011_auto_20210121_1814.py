# Generated by Django 3.1.5 on 2021-01-22 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0010_movementplan_result'),
    ]

    operations = [
        migrations.RenameField(
            model_name='countusagelist',
            old_name='default_uom_conv',
            new_name='luom_no_of_units',
        ),
        migrations.RenameField(
            model_name='countusagelist',
            old_name='po_qty',
            new_name='luom_po_qty',
        ),
        migrations.RenameField(
            model_name='countusagelist',
            old_name='default_uom_price',
            new_name='luom_price',
        ),
        migrations.RenameField(
            model_name='countusagelist',
            old_name='luom_conv',
            new_name='uom_conv',
        ),
        migrations.RemoveField(
            model_name='countusagelist',
            name='default_uom',
        ),
        migrations.AddField(
            model_name='countusagelist',
            name='uom',
            field=models.CharField(default='EA', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='countusagelist',
            name='wt_avg_cost',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]