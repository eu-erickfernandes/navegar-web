from django.urls import path

from .views import *
from .actions import *

app_name = 'route'

urlpatterns = [
    # VIEWS
    path('', search, name= 'search'),
    path('rotas/<int:route_id>/', route, name= 'route'),
    path('rotas/', index, name= 'index'),
    path('rotas/adicionar', add, name= 'add'),
    path('embarcacoes/', boats, name= 'boats'),

    # ACTIONS
    path('route_creation/', route_creation, name='route_creation'),
    path('route_update/<int:route_id>', route_update, name='route_update')
]