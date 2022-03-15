from django.shortcuts import render
from django.http.response import HttpResponse



def index(request):
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
