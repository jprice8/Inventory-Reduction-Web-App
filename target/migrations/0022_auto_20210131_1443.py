# Generated by Django 3.1.5 on 2021-01-31 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0021_auto_20210130_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movementplan',
            name='decision',
            field=models.CharField(choices=[('tenet', 'Ship to a facility outside of the system'), ('system', 'Ship to a facility within the system'), ('sell', 'Sell to a third party vendor'), ('trash', 'Trash the item and write off the books')], default='system', max_length=50),
        ),
        migrations.AlterField(
            model_name='movementplan',
            name='ship_fac',
            field=models.CharField(choices=[('000', 'Not Shipping Within the System'), ('939', 'Baptist Medical Center'), ('971', 'Mission Trail Baptist Hospital'), ('952', 'Saint Lukes Baptist Hospital'), ('872', 'Resolute Health Hospital'), ('968', 'Northeast Baptist Hospital'), ('954', 'North Central Baptist Hospital')], max_length=3),
        ),
    ]
