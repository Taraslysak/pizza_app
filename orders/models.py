from django.db import models

class Meal_type(models.Model):
    meal_type = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.meal_type}'


class Meal_size(models.Model):
    size = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.size}'


class Pizza_option(models.Model):
    option = models.CharField(max_length=128)
    toppings_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.option}'


class Meal(models.Model):
    name = models.CharField(max_length=64)
    meal_type = models.ForeignKey(Meal_type, on_delete=models.CASCADE, null=True)
    price = models.FloatField()

    def __str__(self):
        return f'{self.name} {self.meal_type} - {self.price}USD'

class Cookie(Meal):
    pass


class Pizza(Meal):
    option = models.ForeignKey(Pizza_option, on_delete=models.CASCADE, related_name='pizzas')
    size = models.ForeignKey(Meal_size, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.size} {self.name} {self.meal_type} with {self.option} - {self.price}USD'


class Sub(Meal):
    size = models.ForeignKey(Meal_size, on_delete=models.CASCADE, related_name='subs')
    additional_extras = models.BooleanField(default=False)

def __str__(self):
    return f'{self.size} {self.name} {self.meal_type} - {self.price}USD. Extras allowed: {self.additional_extras}'


class Pasta(Meal):
    pass


class Salad(Meal):
    pass

class Dinner_Platter(Meal):
    size = models.ForeignKey(Meal_size, on_delete=models.CASCADE, related_name='dinner_platters')

    def __str__(self):
        return f'{self.size} {self.name} {self.meal_type} - {self.price}USD'

# class Topping(models.Model):
#         topping = models.CharField(max_length=128)

#         def __str__(self):
#             return f'{self.topping}'
        
#         def say_hello(self):
#             return 'Hello world!'


# class Pizza_style(models.Model):
#     style = models.CharField(max_length=64)

#     def __str__(self):
#         return f'{self.style}'


# class Pizza_option(models.Model):
#     option = models.CharField(max_length=128)
#     toppings_quantity = models.IntegerField(default=0)

#     def __str__(self):
#         return f'{self.option}'


# class Pizza(models.Model):
#     meal_type = models.ForeignKey(Meal_type, on_delete=models.CASCADE, related_name='pizzas')
#     style = models.ForeignKey(Pizza_style, on_delete=models.CASCADE, related_name='pizzas')
#     size = models.ForeignKey(Meal_size, on_delete=models.CASCADE, related_name='pizzas')
#     option = models.ForeignKey(Pizza_option, on_delete=models.CASCADE, related_name='pizzas')
#     price = models.FloatField()
#     topping = models.ManyToManyField(Topping, blank=True, related_name='pizzas')

#     def __str__(self):
#         return f'{self.style} pizza of {self.size} size. Option "{self.option}". Price - {self.price} USD.'

#     @classmethod
#     def of_type_option_and_size(cls, style, option, size):
#         return cls.objects.get(style__style=style, option__option=option, size__size=size)
#     @property
#     def sizes(self):
#         return self.size.all()


# class Extra(models.Model):
#     extra = models.CharField(max_length=64)
#     price = models.FloatField()
#     additional = models.BooleanField()

#     def __str__(self):
#         return f'{self.extra}. Additional: {self.additional}. Price: {self.price}'


# class Sub(models.Model):
#     meal_type = models.ForeignKey(Meal_type, on_delete=models.CASCADE, related_name='subs')
#     name = models.CharField(max_length=64)
#     size = models.ForeignKey(Meal_size, on_delete=models.CASCADE, related_name='subs')
#     base_price = models.FloatField()
#     additional_extras = models.BooleanField()

#     def __str__(self):
#         return f'{self.name} Sub of {self.size} size.  Additional extras: {self.additional_extras}. Price: {self.base_price} USD.'


# class Pasta(models.Model):
#     meal_type = models.ForeignKey(Meal_type, on_delete=models.CASCADE, related_name='pastas')
#     name = models.CharField(max_length=128)
#     price = models.FloatField()

#     def __str__(self):
#         return f'{self.name}. Price: {self.price}'


# class Salad(models.Model):
#     meal_type = models.ForeignKey(Meal_type, on_delete=models.CASCADE, related_name='salads')
#     name = models.CharField(max_length=128)
#     price = models.FloatField()

#     def __str__(self):
#         return f'{self.name}. Price: {self.price}'


# 
    