from django.urls import path

from store import views

app_name = 'store'

urlpatterns = [
    path('', views.store, name='store'),
    path('product/<int:pk>', views.product_page, name='products_page'),
    path('category/<int:pk>', views.category_page, name='category_page')
]