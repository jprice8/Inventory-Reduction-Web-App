# Generated by Django 3.1.5 on 2021-02-12 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0025_auto_20210212_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movementplan',
            name='ship_fac',
            field=models.CharField(choices=[('TEN', 'Shipping to Tenet Facility'), ('DIS', 'Selling or Discarding'), ('939', 'Baptist Medical Center'), ('971', 'Mission Trail Baptist Hospital'), ('952', 'Saint Lukes Baptist Hospital'), ('872', 'Resolute Health Hospital'), ('968', 'Northeast Baptist Hospital'), ('954', 'North Central Baptist Hospital')], max_length=3),
        ),
    ]