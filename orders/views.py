import json

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.db.models import Sum
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



from .models import Pizza, MealSize, Sub, Salad, Pasta, DinnerPlatter, Additive, PizzaTopping, SubExtra, PizzaOption, Order, OrderItem, Meal
from .forms import RegisterForm, LoginForm

# Create your views here.
@login_required(login_url='/login')
def index(request):
    context = {'pizzas': Pizza.display_as_menu(),
        'sizes': MealSize.objects.all(),
        'subs': Sub.display_as_menu(),
        'salads': Salad.display_as_menu(),
        'pastas': Pasta.display_as_menu(),
        'dinner_platters': DinnerPlatter.display_as_menu(),
        'toppings': PizzaTopping.objects.all(),
        'cart_items_count': Order.get_items_count(customer=request.user, issued=False),
    }
    
    return render(request, "orders/index.html", context)


@login_required
def add_item(request, meal_id):
    order = Order.objects.get_or_create(customer=f'{request.user}', issued=False)[0]
    meal = get_object_or_404(Meal, pk=meal_id)
    order_item = OrderItem.objects.create(order=order, meal=meal)
    order.items.add(order_item)
    summ = order.items.aggregate(Sum('meal__price'))
    
    data = {
        'cartStatusCounter': order.items.count(),
        'total': order.calculate_total()
    }
  
    return JsonResponse(data)


@login_required
def remove_item(request, item_id):
    order = Order.objects.get(customer=f'{request.user}', issued=False)
    item = OrderItem.objects.get(pk=item_id)
    order.items.remove(item)

    if order.items.count() > 0:
        data = {
                'cartStatusCounter': order.items.count(),
                'total': order.calculate_total()
                }
    else:
        data = {'total': None}
    return JsonResponse(data)


@login_required
def render_cart(request):
    order =  get_object_or_404(Order,customer=f'{request.user}', issued=False)
    order_items = order.items.all()
    data = {}
    data['total'] = order.calculate_total()
    item_types = {item.meal.meal_type.meal_type for item in order_items}
    if 'Pizza' in item_types:
        data['toppings'] = [{'id': topping.id, 'name': topping.name} for topping in PizzaTopping.objects.all()]

    if 'Sub' in item_types:
        data['extras'] = {}
        data['extras']['basic'] = SubExtra.basic_dict()
        data['extras']['additional'] = SubExtra.additional_dict()
    data['items'] =[]
    for item in order_items:
        try: 
            pizza = item.meal.pizza
            item_dict = pizza.display_as_dict()
            item_dict['id'] = item.id          
            data['items'].append(item_dict)
            continue
        except ObjectDoesNotExist:
            pass
        
        try:
            sub = item.meal.sub
            item_dict = sub.display_as_dict()
            item_dict['id'] = item.id
            data['items'].append(item_dict)
            continue
        except ObjectDoesNotExist:
            pass

        try:
            dinner_platter = item.meal.dinnerplatter
            item_dict = dinner_platter.display_as_dict()
            item_dict['id'] = item.id
            data['items'].append(item_dict)
            continue
        except ObjectDoesNotExist:
            pass

        item_dict = item.meal.display_as_dict()
        item_dict['id'] = item.id
        data['items'].append(item_dict)
    return JsonResponse(data, safe=False)


@login_required
def confirm_purchase(request, methods="POST"):

    updated_order = json.loads(request.body.decode('utf-8'))

    order_from_db = Order.objects.get(customer=f'{request.user}', issued=False)
    order_from_db.total_price = updated_order['total']
    order_from_db.issued = True
    order_from_db.save()

    for item_id in updated_order['items']:
        order_item = OrderItem.objects.get(pk=item_id)
        order_item.additives.clear()
        for additive_id in updated_order['items'][item_id]:
            new_additive = Additive.objects.get(pk=additive_id)
            order_item.additives.add(new_additive)

    print(order_from_db)
    return HttpResponse(status=204)


def register_view(request):
    if request.method == 'POST':

        register_form = RegisterForm(request.POST)
        try:
            assert register_form.is_valid()

            user_info = register_form.cleaned_data
            
            username = user_info['username']
            email = user_info['email']
            password = user_info['password']
            User.objects.create_user(username, email, password)
            user = authenticate(request, username=username, password=password)
            
            login(request, user)

            return HttpResponseRedirect(reverse("index"))

        except (AssertionError, IntegrityError):
        
            register_form = RegisterForm()
            context = {'form': register_form, 'message': 'Invalid credentials!'}
            return render(request, "orders/register.html", context)
        
        except user.PermissionDenied:
            register_form = RegisterForm()
            context = {'form': register_form, 'message': 'Authentification failed!'}
            return render(request, "orders/register.html", context)
       
    else:
        register_form = RegisterForm()
        return render(request, "orders/register.html", {'form': register_form})


def login_view(request):
    if request.method == 'POST':
        
        login_form = LoginForm(request.POST)
        try:
            assert login_form.is_valid()

            user_info = login_form.cleaned_data
            
            user = authenticate(request, username=user_info['username'], password=user_info['password'])
            if user is not None:

                login(request, user)
                messages.add_message(request, messages.SUCCESS, f'Welcome, {user}')
                return HttpResponseRedirect(reverse("index"))
            else:
                messages.add_message(request, messages.ERROR, 'Inalid credentials! Please, check your username and password.')
            return render(request, "orders/login.html", {'form': login_form})

        except AssertionError:
            messages.add_message(request, messages.ERROR, 'Invalid form inputs. Please check your credentials')
            login_form = LoginForm()
            return render(request, "orders/login.html", {'form': login_form})
            
    else:
        login_form = LoginForm()
        return render(request, "orders/login.html", {'form': login_form})


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
