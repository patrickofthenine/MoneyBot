# Generated by Django 3.0.3 on 2020-02-13 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oanda', '0002_auto_20200213_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
