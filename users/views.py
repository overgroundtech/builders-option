from django.shortcuts import redirect, HttpResponseRedirect, render
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.messages import info, error
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from main.models import Category, Order, OrderItem, BillingAddress
from cart.cart import Cart
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


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

    return render(request, 'users/auth.html', context={
        "cart": Cart(request),
        "categories": Category.objects.all()
    })


def sign_up(request):
    if request.POST:
        username = request.POST["register-username"]
        email = request.POST["register-email"]
        password = request.POST["register-password"]
        password1 = request.POST["register-password1"]

        if get_user_model().objects.filter(username=username).exists():
            info(request, 'username already in use')
            return redirect('sign-up')

        if password == password1:
            user = get_user_model().objects.create_user(
                username=username,
                email=email
            )
            user.set_password(password)
            user.save()
            info(request, 'registered successfully')
            login(request, user)
            return redirect('home')
        else:
            error(request, 'passwords did not match')
            return redirect('sign-up')
    else:
        return render(request, 'users/auth.html', context={
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
    billing_address = BillingAddress.objects.get(user_id=user.id)

    context = {
        "orders": orders,
        "order_items": order_items,
        "billing_address": billing_address
    }
    return render(request, 'users/dashboard.html', context)


def edit_billing_address(request):
    if request.method == "POST":
        user = request.user

        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        postcode = request.POST['postcode']
        town = request.POST['phone']
        county = request.POST['county']
        email = request.POST['email']

        billing_address = BillingAddress.objects.get(user_id=user.id)
        billing_address.firstname = firstname
        billing_address.lastname = lastname
        billing_address.postcode = postcode
        billing_address.county = county
        billing_address.town = town
        billing_address.email = email
        billing_address.save()
        info(request, 'Your billing address has been updated')

    return redirect('dashboard')


def edit_account(request):
    if request.POST:
        user = request.user

        email = request.POST['email']
        current_password = request.POST['current-password']
        new_password = request.POST['new-password']
        new_password1 = request.POST['new-password1']

        user.email = email if email else user.email
        if current_password and new_password and new_password1:
            user_obj = authenticate(username=user.username, password=current_password)
            user = get_user_model().objects.get(pk=user_obj.id)
            if new_password == new_password1:
                user.set_password(new_password)
                user.save()
                info(request, 'account updated')
                return redirect(request.GET.get('next')) if request.GET.get('next') else redirect('dashboard')
            else:
                error(request, 'account update failed')
    return redirect('dashboard')


class ResetPasswordView:
    pass
