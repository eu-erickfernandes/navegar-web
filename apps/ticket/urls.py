from django.urls import path

from .views import *
from .actions import *

app_name = 'ticket'

urlpatterns = [
    # VIEWS
    path('', index, name= 'index'),
    path('adicionar/<int:route_boat_weekday_id>/<slug:date>/', add, name= 'add'),
    path('<int:ticket_id>/pdf/', pdf, name= 'pdf'),
    path('passagem/<int:ticket_id>/', ticket, name= 'ticket'),

    # ACTIONS
    path('ticket_creation/<int:route_boat_weekday_id>/<slug:date>/', ticket_creation, name= 'ticket_creation'),
    # path('ticket_cancellation/<int:ticket_id>/', ticket_cancellation, name= 'ticket_cancellation'),
    path('ticket_check/<int:ticket_id>/', ticket_check, name= 'ticket_check'),
    path('ticket_upload/<int:ticket_id>/', ticket_upload, name= 'ticket_upload'),
    path('ticket_update/<int:ticket_id>/<str:new_status>', ticket_update, name= 'ticket_update'),
]