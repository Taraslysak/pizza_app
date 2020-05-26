from django.contrib import admin
from .models import Meal, Meal_size, Topping, Pizza_style, Pizza_option, Pizza, Extra, Sub, Pasta, Salad, Dinner_Platter

admin.site.register(Meal)
admin.site.register(Meal_size)
admin.site.register(Topping)
admin.site.register(Pizza)
admin.site.register(Pizza_style)
admin.site.register(Pizza_option)
admin.site.register(Extra)
admin.site.register(Sub)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Dinner_Platter)