from django.urls import path
from . import views

urlpatterns = [
    path('pizzas/', views.pizza_list, name='pizza_list'),
    path('pizzas/<int:pk>/', views.pizza_detail, name='pizza_detail'),
    path('drinks/', views.drink_list, name='drink_list'),
    path('drinks/<int:pk>/', views.drink_detail, name='drink_detail'),
    path('add_to_cart/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/increase_quantity/<int:item_id>/', views.increase_qunatity, name='increase_quantity'),
    path('cart/decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.order_create, name='order_create'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout')
  ] 