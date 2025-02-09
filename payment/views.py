from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.urls import reverse
from order.models import Order
import uuid
from django.http import HttpResponse

# Create your views here.
def mpesaPayment(request):
    return render(request, 'payment/MpesaPayment.html', {})

def paypalPayment(request, order_id):
    order = Order.objects.get(pk=order_id)
    amount = order.total_price / 130
    products = [item.product.product_name for item in order.orderitem_set.all()]
    host = request.get_host()
    paypal_checkout = {
    'business': settings.PAYPAL_RECEIVER_EMAIL,
    'amount': amount,
    'no_shipping': '2',
    'item_name': ", ".join(products),
    'invoice': str(uuid.uuid4()),
    'currency_code': 'USD',
    'notify_url': f"http://{host}{reverse('paypal-ipn')}",
    'return_url': f"http://{host}{reverse('payment:payment-success', kwargs = {'order_id': order_id})}",
    'cancel_url': f"http://{host}{reverse('payment:payment-failure', kwargs = {'order_id': order_id})}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    return render(request, 'payment/PaypalPayment.html', {"paypal":paypal_payment})

def paymentPaymentFailure(request, order_id):
    return HttpResponse(f"Failed {order_id}")


def paymentSuccess(request, order_id):
    return HttpResponse(f"Success {order_id}")
