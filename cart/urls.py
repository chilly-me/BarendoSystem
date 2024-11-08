from django.urls import path

from cart import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_home, name='cart_home'),
    path('cart_add/', views.add_item, name='add_item'),
    path('remove_item/', views.remove_item, name='remove_item'),
    path('update_cart/', views.update_cart, name='update_cart'),
]