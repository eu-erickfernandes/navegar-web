from re import sub

from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST

from .models import CustomUser
from utils.format import date_format

@require_POST
def user_registration(request):
    # DATA VALIDATION

    name = request.POST.get('name')
    cpf = request.POST.get('cpf')
    birth_date = date_format(request.POST.get('birth_date'))
    email = request.POST.get('email')
    phone = request.POST.get('phone')

    password = request.POST.get('password')
    password_confirmation = request.POST.get('password_confirmation')

    fields = {
        'name': name,
        'cpf': cpf,
        'birth_date': request.POST.get('birth_date'),
        'email': email,
        'phone': phone
    }

    # HANDLING ERRORS
    error_messages = {
        'cpf': 'CPF já cadastrado',
        'birth_date': 'Data inválida',
        'email': 'E-mail já cadastrado',
        'phone': 'Telefone já cadastrado',
        'password_confirmation': 'Os campos de senha não estão iguais',
    }

    if CustomUser.objects.filter(cpf= cpf).exists():
        return render(request, 'authentication/auth.html', {
            'error_message': {'cpf': 'CPF já cadastrado'},
            'fields': fields
        })

    if CustomUser.objects.filter(email= email).exists():
        return render(request, 'authentication/auth.html', {
            'error_message': {'email': 'E-mail já cadastrado'},
            'fields': fields
        })

    if CustomUser.objects.filter(phone= phone).exists():
        return render(request, 'authentication/auth.html', {
            'error_message': {'phone': 'Telefone já cadastrado'},
            'fields': fields
        })
    
    # USER CREATION
    user = CustomUser.objects.create_user(
        name= name,
        cpf= cpf,
        birth_date= birth_date,
        phone= phone,
        email= email,
        password= password
    )

    return redirect(reverse('authentication:signin'))


@require_POST
def user_login(request):
    auth_type = request.POST.get('radio-auth-type')

    error_messages = {
        'auth': 'Credenciais inválidas, tente novamente'
    }

    if auth_type == 'email':
        email = request.POST.get('email')
    elif auth_type == 'phone':
        phone = sub('\D', '', request.POST.get('phone'))

        try:    
            email = CustomUser.objects.get(phone= phone).email
        except:
            return render(request, 'authentication/auth.html', {
                'error_messages': error_messages,
                'login': True
            })
    
    password = request.POST.get('password')

    user = authenticate(request, email= email, password= password)

    if user:
        login(request, user)

        return redirect(reverse('route:search'))
    
    return render(request, 'authentication/auth.html', {
        'error_messages': error_messages,
        'login': True
    })