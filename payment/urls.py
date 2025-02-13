from django.urls import path
from . import views


app_name='payment'

urlpatterns = [
    path('mpesa-page/', views.mpesa_page, name='mpesa_page'),
    path('mpesa-payment/', views.mpesaPayment, name='mpesa_payment'),
    path('paypal/<int:order_id>/', views.paypalPayment, name='paypal'),
    path('paymentSuccess/<int:order_id>/', views.paymentSuccess, name="payment-success"),
    path('paymentFail/<int:order_id>/', views.paymentPaymentFailure, name="payment-failure"),
    path('mpesa_callback/', views.mpesa_callback, name="mpesa_callback")
]
