# Generated by Django 3.0.6 on 2020-06-13 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20200611_1913'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Dinner_Platter',
            new_name='DinnerPlatter',
        ),
        migrations.RenameModel(
            old_name='Meal_size',
            new_name='MealSize',
        ),
        migrations.RenameModel(
            old_name='Meal_type',
            new_name='MealType',
        ),
        migrations.RenameModel(
            old_name='Pizza_option',
            new_name='PizzaOption',
        ),
    ]
