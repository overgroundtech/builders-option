from django.shortcuts import redirect, HttpResponseRedirect, render
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.messages import info, error
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from main.models import Category, Order, OrderItem
from cart.cart import Cart


def sign_in(request):
    if request.method == "GET":
        cache.set('next', request.GET.get('next', None))

    if request.method == "POST":
        username = request.POST['singin-email']
        password = request.POST['singin-password']

        if '@' in username:
            username = get_user_model().objects.get(email=username).username

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            info(request, f'logged in as {user.username}')
            next_url = cache.get('next')
            if next_url:
                cache.delete('next')
                return HttpResponseRedirect(next_url)
            return redirect('home')
        else:
            error(request, 'invalid username or password')

    return render(request, 'main/auth.html', context={
        "cart": Cart(request),
        "categories": Category.objects.all()
    })


def sign_up(request):
    if request.POST:
        username = request.POST["register-username"]
        email = request.POST["register-email"]
        password = request.POST["register-password"]
        password1 = request.POST["register-password1"]

        if password == password1:
            user = get_user_model().objects.create_user(
                username=username,
                email=email
            )
            user.set_password(password)
            user.save()
            info(request, 'registered successfully')
            login(request, user)
        else:
            error(request, 'passwords did not match')
    else:
        return render(request, 'main/auth.html', context={
            "cart": Cart(request),
            "categories": Category.objects.all()
        })


def sign_out(request):
    logout(request)
    return redirect('home')


@login_required(login_url='sign-in')
def dashboard(request):
    user = request.user
    orders = Order.objects.filter(customer_id=user.id)
    order_items = [order_item for order in orders for order_item in OrderItem.objects.filter(order=order)]

    context = {
        "orders": orders,
        "order_items": order_items
    }
    return render(request, 'main/dashboard.html', context)
