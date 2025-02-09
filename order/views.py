from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from CAuthentication.forms import UpdateProfile
from CAuthentication.models import Profile
from cart.cart import Cart
from order.models import Order, OrderItem
from store.models import Product
from django.http import HttpResponse


# Create your views here.
def order_page(request):
    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(user__id=user.id)
        if profile.old_cart != "{}":
            if not profile.phone or not profile.town or not profile.address:
                profile_complete = False
            else:
                profile_complete = True
            payment_date = request.session.get('paymentDate')
            payment_method = request.session.get('paymentMethod')
            if payment_date and payment_method:
                payment_details_complete = True
            else:
                payment_details_complete = False
            cart = Cart(request)
            products = Product.objects.filter(id__in=cart.cart_summary().keys())
            context = {
                'products': products,
                'products_cost': cart.total_cost(),
                'cart': cart.cart_summary(),
                'profile': profile,
                'profile_complete': profile_complete,
                'paymentDate': payment_date,
                'paymentMethod': payment_method,
                'payment_complete': payment_details_complete,
            }
            return render(request, 'order/checkout.html', context)
        else:
            messages.warning(request, "You have to have something in your cart to access this page!")
            return redirect('CAuthentication:home')
    else:
        messages.warning(request, "You have to be authenticated to access this page!")
        return redirect('CAuthentication:home')


def update_address(request):
    profile = Profile.objects.get(user__id=request.user.id)
    profile_form = UpdateProfile(request.POST or None, instance=profile)
    if profile_form.is_valid():
        profile_form.save()
        return redirect('order:order_page')
    else:
        return render(request, 'order/Address.html', {'address_form': profile_form})


def update_payment_details(request):
    if request.method == 'POST':
        PAYMENT_DATE_CHOICES = {
            "now": 'Pay now',
            "on_delivery": 'Pay upon delivery'
        }


        # Get selected values from the POST data
        request.session['paymentDate'] = request.POST.get('paymentDate')
        request.session['paymentMethod'] = request.POST.get('paymentMethod')


        # Mark the session as modified to save changes
        request.session.modified = True

        # Debug print to check session values
        print(request.session.values())
        return redirect('order:order_page')

    return render(request, 'order/Payment Details.html', {})



def payment_processing(request):
    # Access the cart and create a new order
    cart = Cart(request)
    new_order = Order(
        user=request.user,
        total_price=cart.total_cost(),
        payment_date=request.session.get('paymentDate'),
        payment_method=request.session.get('paymentMethod')
    )
    print(f"{new_order.total_price}")
    

    new_order.save()

    # Get cart summary and products in one query
    cart_summary = cart.cart_summary()
    product_ids = cart_summary.keys()
    products = Product.objects.filter(id__in=product_ids)

    # Create OrderItems in bulk
    order_items = []
    for product in products:
        # Retrieve quantity and price directly from cart summary
        item_data = cart_summary.get(str(product.id))
        if item_data:
            order_items.append(OrderItem(
                order=new_order,
                product=product,
                quantity=item_data['quantity'],
                price=item_data['price']
            ))

    # Save all OrderItems at once
    OrderItem.objects.bulk_create(order_items)
    cart.empty_cart()
    return redirect(reverse('payment:paypal', kwargs={'order_id': new_order.id}))

