from django.urls import path

from .views import *
from .actions import *

app_name = 'route'

urlpatterns = [
    # VIEWS
    path('', search, name= 'search'),
    path('embarcacoes/', boats, name= 'boats'),
    path('rotas/', index, name= 'index'),
    path('rotas/adicionar', add, name= 'add'),
    path('rotas/<int:route_id>/', route, name= 'route'),

    # ACTIONS
    path('boat_creation/', boat_creation, name='boat_creation'),
    path('route_creation/', route_creation, name='route_creation'),
    path('route_update/<int:route_id>', route_update, name='route_update')
]