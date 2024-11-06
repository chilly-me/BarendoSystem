from django.urls import path

from store import views

app_name = 'store'

urlpatterns = [
    path('', views.store, name='store'),
    path('product/', views.product_page, name='products_page'),
]