from django.db import models
from django.contrib.auth.models import User


class MealType(models.Model):
    meal_type = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.meal_type}'


class MealSize(models.Model):
    size = models.CharField(max_length=64)
    
    def __str__(self):
        return f'{self.size}'


class PizzaOption(models.Model):
    option = models.CharField(max_length=128)
    toppings_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.option}'


class Meal(models.Model):
    name = models.CharField(max_length=64)
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE, null=True)
    price = models.FloatField()

    def __str__(self):
        return f'{self.name} {self.meal_type} - {self.price} USD'

    def display_as_dict(self):
        result = {
            'type': self.meal_type.meal_type,
            'name': self.name,
            'price': self.price
        }
        return result

    @classmethod
    def display_as_menu(cls):
        return cls.objects.all()
    

class Pizza(Meal):
    option = models.ForeignKey(PizzaOption, on_delete=models.CASCADE, related_name='pizzas')
    size = models.ForeignKey(MealSize, on_delete=models.CASCADE, related_name='pizzas')

    def __str__(self):
        return f'{self.size} {self.name} {self.meal_type} with {self.option} - {self.price} USD'

    def display_as_dict(self):
        result = super().display_as_dict()
        result.update({'option': self.option.option,
                    'size': self.size.size,
                    'toppings_quantity': self.option.toppings_quantity})
        return result
                   

    @classmethod
    def display_as_menu(cls):

        query_set =  cls.objects.all()
        names = set([platter.name for platter in query_set])
        options = [option.option for option in cls.option.get_queryset()]
        sizes = [size.size for size in cls.size.get_queryset()]
        
        menu = {}
        for name in names:
            name_dict = {}
            for option in options:
                option_dict = {}
                for size in sizes:
                    try:
                        option_dict[size] = query_set.get(name=name, option__option=option, size__size=size)
                    except cls.DoesNotExist:
                        print(f'Pizza with these params does not exist: {name}, {option}, {size}')
                        option_dict[size] =[]
                    except cls.MultipleObjectsReturned:
                        print(f'DB have more than one Pizza with these params: {name}, {option}, {size}')
                name_dict[option] = option_dict
            menu[name] = name_dict
        return menu


class Sub(Meal):
    size = models.ForeignKey(MealSize, on_delete=models.CASCADE, related_name='subs')
    additional_extras = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.size} {self.name} {self.meal_type} - {self.price} USD. Extras allowed: {self.additional_extras}'
    
    def display_as_dict(self):
        return {
                    'type': self.meal_type.meal_type,
                    'name': self.name,
                    'size': self.size.size,
                    'price': self.price,
                    'additional_extras': self.additional_extras
                }

    @classmethod
    def display_as_menu(cls):

        query_set =  cls.objects.all()
        names = set([platter.name for platter in query_set])
        sizes = [size.size for size in cls.size.get_queryset()]
        
        menu = {}
        for name in names:
            name_dict = {}
            for size in sizes:
                try:
                    name_dict[size] = query_set.get(name=name, size__size=size)
                except cls.DoesNotExist:
                    print(f'Sub with these params does not exist: {name}, {size}')
                    name_dict[size] = []
                    
                except cls.MultipleObjectsReturned:
                    print(f'DB have more than one Sub with these params: {name}, {size}')
            menu[name] = name_dict
        
        return menu



class Pasta(Meal):
    pass


class Salad(Meal):
    pass

class DinnerPlatter(Meal):
    size = models.ForeignKey(MealSize, on_delete=models.CASCADE, related_name='dinner_platters')

    def __str__(self):
        return f'{self.size} {self.name} {self.meal_type} - {self.price} USD'

    def display_as_dict(self):
        return {
                    'type': self.meal_type.meal_type,
                    'name': self.name,
                    'size': self.size.size,
                    'price': self.price
                }

    @classmethod
    def display_as_menu(cls):

        query_set =  cls.objects.all()
        names = set([platter.name for platter in query_set])
        sizes = [size.size for size in cls.size.get_queryset()]
        
        menu = {}
        for name in names:
            name_dict = {}
            for size in sizes:
                try:
                    name_dict[size] = query_set.get(name=name, size__size=size)
                except cls.DoesNotExist:
                    print(f'Dinner Platter with these params does not exist: {name}, {size}')
                    name_dict[size] = []
                except cls.MultipleObjectsReturned:
                    print(f'DB have more than one Dinner Platter with these params: {name}, {size}')
            menu[name] = name_dict
        return menu

class Additive(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name}'


class PizzaTopping(Additive):
    pass
        
class SubExtra(Additive):
    price = models.FloatField()
    additional = models.BooleanField()

    def __str__(self):
        return f'{self.name}. Additional: {self.additional}. Price: {self.price}'
    
    @classmethod
    def basic_dict(cls):
        return [{'name': extra.name, 'price': extra.price, 'id': extra.id} for extra in cls.objects.filter(additional=False)]

    @classmethod
    def additional_dict(cls):
        return [{'name': extra.name, 'price': extra.price, 'id': extra.id} for extra in cls.objects.filter(additional=True)]


class Order(models.Model):
    customer = models.CharField(max_length=128)
    total_price = models.FloatField(blank=True, null=True)
    issued = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f'Order {self.id}. Customer: {self.customer}. Order issued: {self.issued}. Order closed: {self.closed}. Items: {self.items.get_queryset()}. Total price: {self.total_price}'

    def calculate_total(self):
        total = self.items.aggregate(models.Sum('meal__price'))
        return round(total['meal__price__sum'], 2)

    @classmethod
    def get_items_count(cls, **kwargs):
        try:
            order = cls.objects.get(**kwargs)
            query_result = order.items.count()
            return query_result
        except Order.DoesNotExist:
            return None


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='items')
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, blank=True, related_name='in_orders')
    additives = models.ManyToManyField(Additive, blank=True, related_name='in_orders')

    def __str__(self):
        return f'Meal: {self.meal}'
