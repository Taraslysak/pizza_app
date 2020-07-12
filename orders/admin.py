from django.contrib import admin
from .models import MealSize, Meal, DinnerPlatter, MealType, Pizza, PizzaOption, Salad, Pasta, Sub, PizzaTopping, SubExtra, Order, OrderItem

# admin.site.register(Meal_size)
# admin.site.register(Topping)

# admin.site.register(Pizza_style)

# admin.site.register(Extra)

class Meal_Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    list_filter = ('name', )
    fields = ['name', 'meal_type', 'price']


@admin.register(DinnerPlatter)
class DinnerPlatter_Admin(Meal_Admin):
    list_display = ('id', 'name', 'size', 'price')
    list_filter = ('name', 'size')
    fields = ['name', 'meal_type', 'size', 'price']


@admin.register(Pasta)
class Pasta_Admin(Meal_Admin):
    pass


@admin.register(Salad)
class Salad_Admin(Meal_Admin):
    pass


@admin.register(Pizza)
class Pizza_Admin(Meal_Admin):
    list_display = ('id', 'name', 'size', 'option', 'price')
    list_filter = ('name', 'size', 'option')
    fields = ['name', 'meal_type', 'size', 'option', 'price']


@admin.register(Sub)
class Sub_Admin(Meal_Admin):
    list_display = ('id', 'name', 'size', 'additional_extras', 'price')
    list_filter = ('name', 'size', 'additional_extras')
    fields = ['name', 'meal_type', 'size', 'additional_extras', 'price']


class Additive_Admin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(PizzaTopping)
class PizzaTopping_Admin(Additive_Admin):
    pass


@admin.register(SubExtra)
class SubExtra_Admin(Additive_Admin):
    list_display = ('name', 'additional', 'price')
    list_filter = ['additional']
    fields = ['name', 'additional', 'price']


@admin.register(Order)
class Order_Admin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'issued', 'closed', 'total_price')



#admin.site.register(Meal)

#admin.site.register(Dinner_Platter, Dinner_Platter_Admin)
#admin.site.register(Sub)
#admin.site.register(Pasta)
#admin.site.register(Salad)
#admin.site.register(Pizza)

admin.site.register(MealSize)
admin.site.register(MealType)
admin.site.register(PizzaOption)