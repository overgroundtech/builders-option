from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from cart.cart import Cart
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.messages import info, error
from .models import *


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


def product_detail(request, product_url):
    pk = product_url[(product_url.rindex('~')+1):]
    prod = Product.objects.get(pk=pk)
    images = ProductImages.objects.filter(product=pk)
    similar_products = Product.objects.filter(categories__in=prod.categories.all()).distinct()

    cats = Category.objects.all()
    cart = Cart(request)
# TODO add reviews functionality and social media share
    context = {
        "images": images,
        "product": prod,
        "similar": similar_products,
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

    cats = Category.objects.all()
    cart = Cart(request)
#   Todo create ajax request for updating cart
    context = {
        "cart": cart,
        "categories": cats,
    }
    return render(request, 'main/cart.html', context)


def checkout(request):
    return render(request, 'main/')


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


def search(request):
    cats = Category.objects.all()
    cart = Cart(request)

    context = {
        "cart": cart,
        "categories": cats,
    }

    if request.method == 'GET':
        query = request.GET.get('q')
        prev_path = request.META.get('HTTP_REFERER')
        if (query == '' or query is None) and prev_path is not None:
            return redirect(prev_path)

        if query is not None:
            lookups = Q(name__icontains=query) | Q(description__icontains=query)
            results = Product.objects.filter(lookups).distinct()
            # paginator = Paginator(results, 1)
            # page = request.GET.get('page', 1)
            # try:
            #     prods = paginator.page(page)
            # except PageNotAnInteger:
            #     prods = paginator.page(1)
            # except EmptyPage:
            #     prods = paginator.page(paginator.num_pages)

            context['query'] = query
            context["products"] = results
            return render(request, 'main/search.html', context)
        else:
            return render(request, 'main/search.html', context)
    else:
        return render(request, 'main/search.html', context)



