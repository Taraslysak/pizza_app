# Generated by Django 3.0.6 on 2020-06-15 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20200615_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.FloatField(blank=True),
        ),
    ]