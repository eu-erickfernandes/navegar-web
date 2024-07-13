from django.urls import path

from apps.route.views import *

app_name = 'route'

urlpatterns = [
    path('', search, name= 'search'),
    path('rotas/', index, name= 'index'),
    path('embarcacoes/', boats, name= 'boats')
]