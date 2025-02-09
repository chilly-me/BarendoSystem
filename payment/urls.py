from django.urls import path
from . import views


app_name='payment'

urlpatterns = [
    path('mpesa/', views.mpesaPayment, name='mpesa'),
    path('paypal/<int:order_id>/', views.paypalPayment, name='paypal'),
    path('paymentSuccess/<int:order_id>/', views.paymentSuccess, name="payment-success"),
    path('paymentFail/<int:order_id>/', views.paymentPaymentFailure, name="payment-failure"),
]
