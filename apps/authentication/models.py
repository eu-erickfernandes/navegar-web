from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('A', 'Administrator',),
        ('C', 'Costumer',),
        ('P', 'Passenger',),
        ('S', 'Supplier',)
    ]

    name = models.CharField(max_length= 100)
    birth_date = models.DateField(null= True)
    cpf = models.CharField(max_length= 14, unique= True, null= True, blank= True)

    email = models.EmailField(unique= True, null= True)
    phone = models.CharField(max_length= 16, unique= True, blank= True)

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
    
    def get_translated_role(self):
        ROLE_TRANSLATIONS = [
            ('A', 'Administrador',),
            ('C', 'Cliente',),
            ('P', 'Passageiro',),
            ('S', 'Fornecedor',)
        ]

        for role in ROLE_TRANSLATIONS:
            if role[0] == self.role:
                return role[1]
            
    class Meta:
        ordering = ['name']