# Generated by Django 3.1.5 on 2021-01-24 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0014_auto_20210123_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movementplan',
            name='isMove',
        ),
        migrations.RemoveField(
            model_name='movementplan',
            name='isSell',
        ),
        migrations.RemoveField(
            model_name='movementplan',
            name='isTrash',
        ),
        migrations.AddField(
            model_name='movementplan',
            name='decision',
            field=models.CharField(choices=[('ship', 'Ship'), ('sell', 'Sell'), ('trash', 'Trash')], default='ship', max_length=50),
        ),
    ]
