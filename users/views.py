import requests
from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.messages import info, error


def sign_in(request):

    if request.method == "POST":
        username = request.POST['singin-email']
        password = request.POST['singin-password']

        if '@' in username:
            username = get_user_model().objects.get(email=username).username

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            info(request, f'login is as {user.username}')
            return HttpResponseRedirect(next_url) if next_url is not None else redirect('home')
        else:
            error(request, 'login failed')

    return redirect('home')


def sign_up(request):
    return None


def sign_out(request):
    logout(request)
    return redirect('home')
