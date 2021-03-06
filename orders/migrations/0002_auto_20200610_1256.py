# Generated by Django 3.0.6 on 2020-06-10 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='meal_size',
        ),
        migrations.AddField(
            model_name='meal',
            name='meal_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Meal_type'),
        ),
        migrations.CreateModel(
            name='Dinner_Platter',
            fields=[
                ('meal_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.Meal')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dinner_platters', to='orders.Meal_size')),
            ],
            bases=('orders.meal',),
        ),
    ]
