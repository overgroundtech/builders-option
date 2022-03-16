import requests
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.messages import info, error


def sign_in(request):
    cache = {}
    if request.method == 'GET':
        cache['next'] = request.GET.get('next', None)

    if request.method == "POST":
        username = request.POST['singin-email']
        password = request.POST['singin-password']

        if '@' in username:
            username = get_user_model().objects.get(email=username).username

        user = authenticate(username=username, password=password)

        if user is not None:
            login(user)
            next_url = cache['next']
            info(request, f'login is as {user.username}')
            return HttpResponseRedirect(next_url) if next_url else HttpResponseRedirect(request.GET.get('next', None))
        else:
            error(request, 'login failed')

    return HttpResponseRedirect(request.path)


def sign_up(request):
    return None


def sign_out(request):
    pass