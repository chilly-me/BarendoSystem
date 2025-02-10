from django.urls import path

from order import views

app_name = 'order'

urlpatterns = [
    path('', views.order_page, name='order_page'),
    path('update_address/', views.update_address, name='update_address'),
    path('update_payment_details/', views.update_payment_details, name='update_payment_details'),
    path('payment/', views.payment_processing, name='payment_processing'),
    path('pre-paid-pending-orders/', views.pre_paid_pending_orders, name="pre-paid-pending-orders"),
    path('pay-on-delivery-pending-orders/', views.pay_on_delivery_pending_orders, name="pay-on-delivery-pending-orders"),
    path('order/<int:order_id>', views.specific_order, name="specific-order"),
    path('cancel-order/<int:order_id>', views.cancel_order, name="cancel-order"),
    path('shipped/', views.shipped_orders, name="shipped-orders"),
    path('cancelled/', views.cancelled_orders, name="cancelled-orders"),
]