from django.urls import path

from .views import *

app_name = 'route'

urlpatterns = [
    # VIEWS
    path('', search, name= 'search'),
    path('rotas/', index, name= 'index'),
    path('embarcacoes/', boats, name= 'boats')
]