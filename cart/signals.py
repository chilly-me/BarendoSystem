from django.contrib.auth import user_logged_in
from django.dispatch import receiver

from cart.cart import Cart


@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    cart = Cart(request)
    cart.sync_cart_with_profile()
    print("In the on_user_login signal")


