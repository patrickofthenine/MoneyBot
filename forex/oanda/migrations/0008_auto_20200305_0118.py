# Generated by Django 3.0.3 on 2020-03-05 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oanda', '0007_auto_20200304_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candle',
            name='batch',
            field=models.IntegerField(max_length=50),
        ),
    ]