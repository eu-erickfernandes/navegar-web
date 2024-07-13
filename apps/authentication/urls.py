from django.urls import path

from .views import *
from .actions import *

app_name = 'authentication'

urlpatterns = [
    # VIEWS
    path('', index, name= 'index'),
    path('cadastro/', registration, name= 'registration'),
    path('entrar/', signin, name= 'signin'),
    path('painel/', panel, name= 'panel'),
    path('sair/', user_logout, name= 'user_logout'),

    # ACTIONS
    path('user_registration/', user_registration, name= 'user_registration'),
    path('user_login/', user_login, name= 'user_login'),
]