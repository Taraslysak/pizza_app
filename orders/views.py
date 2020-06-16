from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



from .models import Pizza, MealSize, Sub, Salad, Pasta, DinnerPlatter, PizzaTopping, SubExtra, PizzaOption, Order, OrderItem, Meal
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
def update_cart(request, meal_id):
    order = Order.objects.get_or_create(customer=f'{request.user}', issued=False)[0]
    meal = Meal.objects.get(pk=meal_id)
    order_item = OrderItem.objects.create(order=order, meal=meal)
    
    order.items.add(order_item)

    print(order)
    data = {'answer': f'we`ve got smth! {meal_id}'}

    return JsonResponse(data)

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



