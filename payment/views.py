from order.models import Order
from . import MpesaAuthorization
from django.conf import settings

from django.shortcuts import render, redirect
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
import uuid, datetime, base64
from django.http import HttpResponse
import requests

# Handles API POST request
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import JsonResponse
import random

# def mpesaPayment(request):
#     if request.method == "POST":
#         request_id = "1234567890"  # Replace with actual API response
#         return JsonResponse({"request_id": request_id})

# def check_payment_status(request):
#     if request.method == "POST":
#         request_id = request.POST.get("request_id")
#         status = random.choice(["Pending", "Success", "Failed"])  # Simulating API response
#         return JsonResponse({"status": status})

# Create your views here.
def mpesa_page(request):
    return render(request, 'payment/MpesaPayment.html', {})


def mpesaPayment(request):
    if request.method == "POST":
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        shortCode = "174379"
        stk_password = base64.b64encode(f"{shortCode}{passkey}{timestamp}".encode()).decode()
        host = request.get_host()
        call_back_url = f"https://{host}/payment/mpesa_callback/"
        print(f"In mpesa payment view")
        print(f"This is the current host: {host}")
        body =  {
                    "BusinessShortCode": shortCode,
                    "Password": stk_password,
                    "Timestamp": timestamp,
                    "TransactionType": "CustomerPayBillOnline",
                    "Amount": 1,
                    "PartyA": 254799359792,
                    "PartyB": 174379,
                    "PhoneNumber": 254799359792,
                    "CallBackURL": call_back_url,
                    "AccountReference": "BarendoSystems",
                    "TransactionDesc": "test" 
                }
        token = MpesaAuthorization.generate_access_token()
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        response = requests.post(url, json=body, headers=headers)
        response_dict = response.json()  
        print(response_dict)
        CheckoutRequestID = response_dict["CheckoutRequestID"]
        return JsonResponse({"request_id":CheckoutRequestID})


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


@csrf_exempt
def mpesa_callback(request):
    print(f"In mpesa_callback")
    print(f"{request}")
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            print(f"The data receiverd: {data}")

            return JsonResponse({"message": "Callback received successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)



def mpesa_query(request):
    if request.method == "POST":
        print("In query block")
        request_id = request.POST.get("request_id")
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        shortCode = "174379"
        stk_password = base64.b64encode(f"{shortCode}{passkey}{timestamp}".encode()).decode()

        body = {
            "BusinessShortCode" : shortCode,
            "Password" : stk_password,
            "Timestamp" : timestamp,
            "CheckoutRequestID": request_id
        }
        token = MpesaAuthorization.generate_access_token()
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=body, headers=headers)
        print("The response given {}".format(response))
        return JsonResponse(response)

