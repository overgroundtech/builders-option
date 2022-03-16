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
    return redirect('home')


def sign_out(request):
    logout(request)
    return redirect('home')
