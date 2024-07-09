from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST

from .models import CustomUser, Person
from utils.format import date_format


@require_POST
def user_registration(request):
    name = request.POST.get('name')
    cpf = request.POST.get('cpf')

    birth_date = date_format(request.POST.get('birth_date'))

    person = Person.objects.create(
        name= name,
        cpf= cpf,
        birth_date= birth_date
    )

    email = request.POST.get('email')
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    password_confirmation = request.POST.get('password_confirmation')

    user = CustomUser.objects.create_user(
        person= person,
        phone= phone,
        email= email,
        password= password
    )

    return redirect(reverse('authentication:signin'))
    # return redirect(reverse('authentication:registration'))


@require_POST
def user_login(request):
    auth_type = request.POST.get('radio-auth-type')

    if auth_type == 'email':
        email = request.POST.get('email')
    elif auth_type == 'phone':
        phone = request.POST.get('phone')

        try:    
            email = CustomUser.objects.get(phone= phone).email
        except:
            return redirect(reverse('authentication:signin'))
    
    password = request.POST.get('password')

    user = authenticate(request, email= email, password= password)

    if user:
        login(request, user)

        return redirect(reverse('route:index'))
    
    return redirect(reverse('authentication:signin'))