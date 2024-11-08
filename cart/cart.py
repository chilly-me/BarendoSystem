from store.models import Product


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session

        if 'cart_data' in self.session:
            self.cart_data = self.session['cart_data']
        else:
            self.cart_data = self.session['cart_data'] = {}

        self.session.modified = True

    def cart_summary(self):
        # if self,
        return self.cart_data

    def total_cost(self):
        return sum(int(x['price']) for x in self.cart_data.values())

    def add_item(self, product, quantity):
        product_id = str(product.id)
        price = int(product.price)
        if product_id in self.cart_data:
            pass
        else:
            price = price * int(quantity)
            self.cart_data[product_id] = {'price': float(price), 'quantity': quantity, 'name': product.product_name}

        self.session.modified = True

    def remove_cart(self, product):
        product_id = str(product.id)
        if product_id in self.cart_data:
            del self.cart_data[product_id]
        else:
            pass
        self.session.modified = True


    def update_cart(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart_data:
            price = product.price * int(quantity)
            self.cart_data[product_id]['price'] = float(price)
            self.cart_data[product_id]['quantity'] = quantity
        else:
            pass

        self.session.modified = True

    # def delete_cart(self):
    #     pass

    def __len__(self):
        return len(self.cart_data)
