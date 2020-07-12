from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("add-item/<int:meal_id>", views.add_item, name="add_item"),
    path("remove-item/<int:item_id>", views.remove_item, name="remove_item"),
    path("render-cart", views.render_cart, name="render_cart"),
    path("confirm-purchase", views.confirm_purchase, name="confirm_purchase")
]    
