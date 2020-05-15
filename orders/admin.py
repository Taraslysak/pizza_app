from django.contrib import admin

from .models import Meal, Meal_size, Topping, Pizza_style, Pizza_option, Pizza

admin.site.register(Meal)
admin.site.register(Meal_size)
admin.site.register(Topping)
admin.site.register(Pizza)
admin.site.register(Pizza_style)
admin.site.register(Pizza_option)
# Register your models here.
