from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST

from .models import CustomUser


@require_POST
def user_registration(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = CustomUser.objects.create_user(
        name= name,
        email= email,
        password= password
    )

    return redirect(reverse('authentication:login'))


@require_POST
def user_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate(request, email= email, password= password)

    if user:
        login(request, user)

        return redirect(reverse('route:index'))
    
    return redirect(reverse('authentication:signin'))