import ast
import json

from CAuthentication.models import Profile
from store.models import Product

from django.shortcuts import get_object_or_404


def save_to_profile(self):
    if self.user.is_authenticated:
        user_profile = get_object_or_404(Profile, user=self.user)
        user_profile.old_cart = self.cart_data
        user_profile.save()


class Cart:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.session = request.session
        self.cart_data = self.session.setdefault('cart_data', {})
        self.session.modified = True

    def cart_summary(self):
        return self.cart_data

    def total_cost(self):
        return sum(float(item['price']) for item in self.cart_data.values())

    def add_item(self, product, quantity):
        product_id = str(product.id)
        price = float(product.price) * int(quantity)

        if product_id not in self.cart_data:
            self.cart_data[product_id] = {'price': price, 'quantity': quantity, 'name': product.product_name}
            self.session.modified = True

        save_to_profile(self)

    def remove_item(self, product):
        product_id = str(product.id)
        if product_id in self.cart_data:
            del self.cart_data[product_id]
            self.session.modified = True

        save_to_profile(self)

    def update_cart(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart_data:
            price = float(product.price) * int(quantity)
            self.cart_data[product_id]['price'] = price
            self.cart_data[product_id]['quantity'] = quantity
            self.session.modified = True

        save_to_profile(self)

    def sync_cart_with_profile(self):
        """
           This method syncs the session cart data with the user's profile cart data.
           - It retains any session cart data if present.
           - It merges the user's saved cart data from their profile (if authenticated) into the session.
           - Ensures no duplicates by merging quantities if the product is in both the session and the profile.
           """
        global profile_cart_data
        if self.user.is_authenticated:
            user_profile = Profile.objects.get(user=self.user)
            if user_profile.old_cart:
                try:
                    profile_cart_data = json.loads(user_profile.old_cart)
                except json.JSONDecodeError:
                    try:
                        profile_cart_data = ast.literal_eval(user_profile.old_cart)
                    except Exception:
                        self.cart_data = {}
                        self.session['cart_data'] = self.cart_data
                        self.session.modified = True
                        save_to_profile(self)
                if profile_cart_data:
                    for product_id, profile_item in profile_cart_data.items():
                        if product_id in self.cart_data:
                            cart_quantity = int(self.cart_data[product_id]['quantity'])
                            profile_quantity = int(profile_item['quantity'])
                            total = cart_quantity + profile_quantity
                            self.cart_data[product_id]['quantity'] = total
                            self.cart_data[product_id]['price'] = self.cart_data[product_id]['quantity'] * profile_item[
                                'price']
                            save_to_profile(self)
                        else:
                            self.cart_data[product_id] = profile_item
                            self.session['cart_data'] = self.cart_data
                            self.session.modified = True
                            save_to_profile(self)
            else:
                if 'cart_data' in self.session:
                    self.cart_data = self.session['cart_data']
                else:
                    self.cart_data = {}
                self.session.modified = True
                save_to_profile(self)

        else:
            if 'cart_data' in self.session:
                self.cart_data = self.session['cart_data']
            else:
                self.cart_data = {}
            self.session.modified = True
            save_to_profile(self)

    def empty_cart(self):
        self.cart_data = {}
        self.session['cart_data'] = self.cart_data
        self.session.modified = True

        if self.user.is_authenticated:
            user_profile = get_object_or_404(Profile, user=self.user)
            user_profile.old_cart = ''
            user_profile.save()

    def __len__(self):
        return len(self.cart_data)
