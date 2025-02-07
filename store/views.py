from django.shortcuts import render

from store.models import Product, Category


# Create your views here.

def store(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'store/store.html', {'products': products, 'categories': categories})


def product_page(request, pk):
    product = Product.objects.get(pk=pk)
    related_products = Product.objects.filter(category_id=product.category_id).exclude(pk=product.pk)
    return render(request, 'store/products_page.html', {"product": product, "related_products": related_products})

def category_page(request, pk):
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(category__id=category.id)
    return render(request, 'store/category_page.html', {'products':products, 'category': category})