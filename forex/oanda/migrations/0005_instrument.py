# Generated by Django 3.0.3 on 2020-02-14 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oanda', '0004_auto_20200213_2348'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
    ]