# Generated by Django 3.0.6 on 2020-06-29 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_auto_20200624_1058'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='additive',
            new_name='additives',
        ),
    ]
