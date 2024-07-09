from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager

class Person(models.Model):
    name = models.CharField(max_length= 100)
    birth_date = models.DateField(null= True)
    cpf = models.CharField(max_length= 14, null= True, unique= True)

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('P', 'Passenger'),
        ('A', 'Administrator')
    ]
    person = models.OneToOneField(Person, null= True, on_delete= models.CASCADE)
    email = models.EmailField(unique= True)
    phone = models.CharField(max_length= 16, unique= True, null= True)

    role = models.CharField(max_length=1, choices= ROLE_CHOICES, default= 'P')

    is_staff = models.BooleanField(default= False)
    is_active = models.BooleanField(default= True)
    date_joined = models.DateTimeField(default= timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()