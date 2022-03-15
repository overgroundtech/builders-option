from django.shortcuts import render
from django.http.response import HttpResponse
from .models import *


def index(request):
    prods = Product.objects.all()
    cats = Category.objects.all()


    context = {}
    return render(request, 'main/index.html', context)


def products(request):
    return HttpResponse


def categories(request):
    return HttpResponse


def cart(request):
    return HttpResponse


def checkout(request):
    return HttpResponse
