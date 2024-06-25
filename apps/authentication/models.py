from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length= 100)
    email = models.EmailField(unique= True)


    is_staff = models.BooleanField(default= False)
    is_active = models.BooleanField(default= True)
    date_joined = models.DateTimeField(default= timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()