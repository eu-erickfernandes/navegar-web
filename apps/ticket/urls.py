from django.urls import path

from .views import *
from .actions import *

app_name = 'ticket'

urlpatterns = [
    # VIEWS
    path('', index, name= 'index'),
    path('adicionar/<int:route_boat_weekday_id>/<slug:date>/', add, name= 'add'),
    path('<int:ticket_id>/pdf/', pdf, name= 'pdf'),

    # ACTIONS
    path('ticket_creation/<int:route_boat_weekday_id>/<slug:date>/', ticket_creation, name= 'ticket_creation')
]