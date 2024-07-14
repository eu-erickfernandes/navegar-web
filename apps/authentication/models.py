from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('A', 'Administrator',),
        ('P', 'Passenger',),
        ('S', 'Supplier',)
    ]

    name = models.CharField(max_length= 100)
    birth_date = models.DateField()
    cpf = models.CharField(max_length= 14, unique= True)

    email = models.EmailField(unique= True)
    phone = models.CharField(max_length= 16, unique= True)

    role = models.CharField(max_length=1, choices= ROLE_CHOICES, default= 'P')
    upload_ticket = models.BooleanField(default= False)

    # CUSTOM USER SETTINGS
    is_staff = models.BooleanField(default= False)
    is_active = models.BooleanField(default= True)
    date_joined = models.DateTimeField(default= timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'birth_date', 'cpf', 'phone']

    objects = CustomUserManager()

    def __str__(self):
        return self.name