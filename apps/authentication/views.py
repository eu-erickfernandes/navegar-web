from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .decorators import redirect_authenticated_user, required_user_roles
from .models import *

@redirect_authenticated_user
def registration(request):
    return render(request, 'authentication/auth.html')


@redirect_authenticated_user
def signin(request):
    login = True

    return render(request, 'authentication/auth.html', {'login': login})


@login_required
def user_logout(request):
    logout(request)

    return redirect(reverse('authentication:signin'))


@login_required
def panel(request):
    return render(request, 'authentication/panel.html')


@login_required
@required_user_roles('A')
def index(request):
    users = CustomUser.objects.all().exclude(is_superuser= True)

    return render(request, 'authentication/index.html', {
        'users': users
    })


@login_required
@required_user_roles('A')
def user(request, user_id):
    try:
        user = CustomUser.objects.get(id= user_id)
    except:
        return redirect(reverse('authentication:index'))
    
    roles = []

    for role in CustomUser.ROLE_CHOICES:
        if role[0] == 'A':
            roles.append(('A', 'Administrador'))

        if role[0] == 'S':
            roles.append(('S', 'Fornecedor'))

        if role[0] == 'C':
            roles.append(('C', 'Cliente'))

    return render(request, 'authentication/user.html', {
        'hidden_navbar': True,
        'user': user,
        'roles': roles
    })