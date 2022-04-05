from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from cart.cart import Cart
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.contrib.messages import info, error


def index(request):
    products_list = Product.objects.all()
    cats = Category.objects.all()
    cart = Cart(request)

    page = request.GET.get('page', 1)
    paginator = Paginator(products_list, 8)
    try:
        prods = paginator.page(page)
    except PageNotAnInteger:
        prods = paginator.page(1)
    except EmptyPage:
        prods = paginator.page(paginator.num_pages)

    context = {
        "products": prods,
        "categories": cats,
        "cart": cart
    }
    return render(request, 'main/index.html', context)


def products(request, product_url):
    pk = product_url[(product_url.rindex('~')+1):]
    prod = Product.objects.get(pk=pk)
    images = ProductImages.objects.filter(product=pk)

    cats = Category.objects.all()
    cart = Cart(request)

    context = {
        "images": images,
        "product": prod,
        "cart": cart,
        "categories": cats
    }

    if request.method == "POST":
        quantity = request.POST['qty']
        cart.add(product=prod, quantity=quantity, unit_price=prod.price)
        info(request, 'product was added to cart!')
        return render(request, 'main/product-detail.html', context)
    return render(request, 'main/product-detail.html', context)


def categories(request):
    return HttpResponse('categories')


def cart_detail(request):
    return HttpResponse('cart detail')


def checkout(request):
    return HttpResponse('checkout')


def add_item(request, prod_id, quantity):
    cart = Cart(request)
    prod = Product.objects.get(pk=prod_id)
    cart.add(product=prod, quantity=quantity, unit_price=prod.price)
    info(request, 'item was added to cart')
    return redirect(request.GET.get('next'))


def remove_item(request, prod_id):
    cart = Cart(request)
    prod = Product.objects.get(pk=prod_id)
    cart.remove(product=prod)
    info(request, 'item was remove from cart')
    return redirect(request.GET.get('next'))

