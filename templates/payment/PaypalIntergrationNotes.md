
Install Paypal Application:

pip install django-paypal

Add the paypal application to settings.paypal
paypal.standard.ipn

Make the necessary migrations

add the paypal to  urls.paypal
inlude('paypal.standard.ipn.urls')

in settings.paypal

define the following:

PAYPAL_RECEIVER_EMAIL = "example@gmail.com"
PAYPAL_TEST = True # in development

PREPARING PAYPAL FORM OBJECT
in your views.py 

from paypal.standard.forms import PayPalPaymentsForm

# To get the host that is loading django at the time
host = request.get_host()

create a dictionary in one function

exapmple
paypal_checkout = {
    'business': the_email_address_to_receive_funds,
    'amount': amount_to_be_charged,
    'item_name': product_name,
    'invoice': unique_id_for_the_transaction,
    'currency_code': 'KES',
    'notify_url': f"http://{host}{reverse('paypal-ipn)}",
    'return_url': f"http://{host}{reverse('payment-success-url', kwargs = {'argument': 'value'})}",
    'cancel_url': f"http://{host}{reverse('payment-failed-url', kwargs = {'argument': 'value'})}",
}

paypal_payment = PaypalPaymentForm(initial=paypal_checkout)

# pass paypal_payment as context


in your template:
{{context.render}}