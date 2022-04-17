from django.shortcuts import render, redirect
from cart.cart import Cart
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.messages import info, error
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    products_list = Product.objects.all()
    on_deals = Product.objects.filter(on_deals=True)
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
        "cart": cart,
        "on_deals": on_deals
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


def categories(request, category_url):
    pk = category_url[(category_url.rindex('~') + 1):]
    category = Category.objects.get(pk=pk)

    prod_list = Product.objects.filter(categories__in=[category]).distinct()
    paginator = Paginator(prod_list, 12)
    page = request.GET.get('page', 1)

    try:
        prods = paginator.page(page)
    except PageNotAnInteger:
        prods = paginator.page(1)
    except EmptyPage:
        prods = paginator.page(paginator.num_pages)

    cart = Cart(request)
    cats = Category.objects.all()
    context = {
        "cart": cart,
        "categories": cats,
        "products": prods,
        "category": category
    }
    return render(request, 'main/category.html', context)


def cart_detail(request):

    cats = Category.objects.all()
    cart = Cart(request)
#   Todo create ajax request for updating cart
    context = {
        "cart": cart,
        "categories": cats,
    }
    return render(request, 'main/cart.html', context)


@login_required(login_url='/users/sign-in')
def checkout(request):
    cats = Category.objects.all()
    cart = Cart(request)

    context = {
        "cart": cart,
        "categories": cats
    }

    user = request.user

    try:
        bill_add = BillingAddress.objects.get(user_id=user.id)
        context['billing_address'] = bill_add
    except BillingAddress.DoesNotExist:
        context['billing_address'] = None

    if request.POST:
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        town = request.POST['town']
        county = request.POST['county']
        postcode = request.POST['postcode']
        phone = request.POST['phone']
        email = request.POST['email']
        notes = request.POST['notes']

        try:
            bill_add = BillingAddress.objects.get(user_id=user.id)
            context['billing_address'] = bill_add
            bill_add.firstname = firstname
            bill_add.lastname = lastname
            bill_add.county = county
            bill_add.town = town
            bill_add.email = email
            bill_add.phone = phone
            bill_add.save()
        except BillingAddress.DoesNotExist:
            bill_add = BillingAddress(
                user=user,
                firstname=firstname,
                lastname=lastname,
                postcode=postcode,
                town=town,
                county=county,
                phone=phone,
                email=email
            )
            bill_add.save()

    return render(request, 'main/checkout.html', context)


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



