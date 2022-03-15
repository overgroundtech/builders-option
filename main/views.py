from django.shortcuts import render
from django.http.response import HttpResponse
from cart.cart import Cart
from .models import *


def index(request):
    prods = Product.objects.all()
    cats = Category.objects.all()
    cart = Cart(request)

    context = {
        "products": prods,
        "categories": cats,
        "cart": cart
    }
    return render(request, 'main/index.html', context)


def products(request):
    return HttpResponse


def categories(request):
    return HttpResponse


def cart_detail(request):
    return HttpResponse


def checkout(request):
    return HttpResponse
