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
    price = models.FloatField()

    def __str__(self):
        return f'{self.style} pizza of {self.size} size. Option "{self.option}". Price - {self.price} USD.'


class Extra(models.Model):
    extra = models.CharField(max_length=64)
    price = models.FloatField()
    additional = models.BooleanField()

    def __str__(self):
        return f'{self.extra}. Additional: {self.additional}. Price: {self.price}'


class Sub(models.Model):
    name = models.CharField(max_length=64)
    size = models.ForeignKey(Meal_size, on_delete=models.CASCADE, related_name='subs')
    base_price = models.FloatField()
    additional_extras = models.BooleanField()

    def __str__(self):
        return f'{self.name} Sub of {self.size} size.  Additional extras: {self.additional_extras}. Price: {self.base_price} USD.'


class Pasta(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()

    def __str__(self):
        return f'{self.name}. Price: {self.price}'


class Salad(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()

    def __str__(self):
        return f'{self.name}. Price: {self.price}'


class Dinner_Platter(models.Model):
    name = models.CharField(max_length=128)
    size = models.ForeignKey(Meal_size, on_delete=models.CASCADE, related_name='dinner_platters')
    price = models.FloatField()

    def __str__(self):
        return f'{self.name} platter. Size: {self.size}. Price: {self.price}'
    