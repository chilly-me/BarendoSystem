from django.urls import path

from order import views

app_name = 'order'

urlpatterns = [
    path('', views.order_page, name='order_page'),
    path('update_address/', views.update_address, name='update_address'),
    path('update_payment_details/', views.update_payment_details, name='update_payment_details'),
    path('payment/', views.payment_processing, name='payment_processing')
]