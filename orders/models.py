from django.db import models

# Create your models here.
class Meal(models.Model):
    meal_name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.meal_name}'


class Meal_size(models.Model):
    size = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.size}'


class Topping(models.Model):
    topping = models.CharField(max_length=128)

    def __str__(self):
       return f'{self.topping}' 


class Pizza_style(models.Model):
    style = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.style}'


class Pizza_option(models.Model):
    option = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.option}'


class Pizza(models.Model):
    style = models.ForeignKey(Pizza_style, on_delete=models.CASCADE, related_name='pizzas')
    size = models.ForeignKey(Meal_size, on_delete=models.CASCADE, related_name='pizzas')
    option = models.ForeignKey(Pizza_option, on_delete=models.CASCADE, related_name='pizzas')
    price = models.IntegerField()

    def __str__(self):
        return f'This is {self.style} pizza of {self.size} size. Its option is "{self.option}" and price - {self.price} USD.'

