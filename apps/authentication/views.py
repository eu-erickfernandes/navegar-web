from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .decorators import redirect_authenticated_user
from .models import *

@redirect_authenticated_user
def registration(request):
    return render(request, 'authentication/auth.html')


@redirect_authenticated_user
def signin(request):
    login = True

    return render(request, 'authentication/auth.html', {'login': login})


def user_logout(request):
    logout(request)

    return redirect(reverse('authentication:signin'))


@login_required
def panel(request):
    return render(request, 'authentication/panel.html')


@login_required
def index(request):
    users = CustomUser.objects.all().exclude(is_superuser= True)

    return render(request, 'authentication/index.html',{
        'users': users
    })