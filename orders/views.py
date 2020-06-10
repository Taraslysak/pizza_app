from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

#from .models import Pizza, Meal_size, Sub, Salad, Pasta, Dinner_Platter, Topping, Extra, Pizza_style, Pizza_option
from .forms import RegisterForm, LoginForm

# Create your views here.
@login_required(login_url='/login')
def index(request):

    # sizes = Meal_size.objects.all()
    # pizza_styles = Pizza_style.objects.all()
    # pizza_options = Pizza_option.objects.all()
    
    # pizzas = {}

    # for pizza_style in pizza_styles:
    #     style = {}
    #     for pizza_option in pizza_options:
    #         option = {}
    #         for size in sizes:
    #             option[size.size] = Pizza.of_type_option_and_size(pizza_style, pizza_option, size)
    #         style[pizza_option.option] = option    
    #     pizzas[pizza_style.style] = style
    

    context = None
    # {'pizzas': pizzas,
    #     'sizes': sizes,
    #     'subs': Sub.objects.all(),
    #     'salads': Salad.objects.all(),
    #     'pastas': Pasta.objects.all(),
    #     'dinner_platters': Dinner_Platter.objects.all(),
    #     'toppings': Topping.objects.all(),
    # }
    
    return render(request, "orders/index.html", context)


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



