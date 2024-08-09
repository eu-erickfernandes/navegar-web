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
    path('<int:user_id>/', user, name= 'user'),

    # ACTIONS
    path('user_registration/', user_registration, name= 'user_registration'),
    path('user_login/', user_login, name= 'user_login'),
    path('user_update/<int:user_id>', user_update, name= 'user_update'),
]