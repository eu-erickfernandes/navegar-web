from django.urls import path

from .views import *
from .actions import *

app_name = 'authentication'

urlpatterns = [
    # VIEWS
    path('', index, name= 'index'),
    path('cadastro/', registration, name= 'registration'),
    path('login/', signin, name= 'signin'),
    path('sair/', user_logout, name= 'logout'),

    # ACTIONS
    path('user_registration/', user_registration, name= 'user_registration'),
    path('user_login/', user_login, name= 'user_login'),
]