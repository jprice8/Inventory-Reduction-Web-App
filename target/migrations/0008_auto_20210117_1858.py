# Generated by Django 3.1.5 on 2021-01-18 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0007_movementplan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movementplan',
            name='ship_fac',
            field=models.CharField(choices=[('000', 'Not Shipping'), ('939', 'Baptist Medical Center'), ('971', 'Mission Trail Baptist Hospital'), ('952', 'Saint Lukes Baptist Hospital'), ('872', 'Resolute Health Hospital'), ('968', 'Northeast Baptist Hospital'), ('954', 'North Central Baptist Hospital')], max_length=3),
        ),
    ]
