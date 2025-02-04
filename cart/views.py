from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from cart.cart import Cart
from store.models import Product


# Create your views here.
def cart_home(request):
    cart = Cart(request)
    cart_summary = cart.cart_summary()
    print(cart.total_cost())
    products = Product.objects.filter(id__in=cart_summary.keys())
    return render(request, 'cart/cart_home.html',
                  {"products": products, "cart_sum": cart_summary, "cost": cart.total_cost()})


def add_item(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = request.POST.get('product_qty')
        product = get_object_or_404(Product, id=product_id)
        cart.add_item(product=product, quantity=product_qty)
        response = JsonResponse({'cart_quantity': cart.__len__()})
        return response
    else:
        return redirect('store:store')


def remove_item(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        cart.remove_item(product)
        response = JsonResponse({'cart_quantity': cart.__len__()})
        return response


def update_cart(request):
    cart = Cart(request)
    print(request.POST)
    if request.POST.get('action') == 'post':
        print("In the post")
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(Product, id=product_id)
        cart.update_cart(product, quantity)
        response = JsonResponse({'cart_quantity': cart.__len__()})
        return response
    else:
        return HttpResponse("Failed")
