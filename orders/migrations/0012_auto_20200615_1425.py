# Generated by Django 3.0.6 on 2020-06-15 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20200615_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.CharField(max_length=128),
        ),
    ]