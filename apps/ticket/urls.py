from django.urls import path

from .views import *
from .actions import *

app_name = 'ticket'

urlpatterns = [
    # VIEWS
    path('', index, name= 'index'),
    path('adicionar/<int:route_boat_weekday_id>/<slug:date>/', add, name= 'add'),
    path('<int:ticket_id>/pdf/', pdf, name= 'pdf'),
    path('<int:ticket_id>/', ticket, name= 'ticket'),
    path('remarcacao/<int:ticket_id>/', rebooking, name= 'rebooking'),

    # ACTIONS
    path('ticket_creation/<int:route_boat_weekday_id>/<slug:date>/', ticket_creation, name= 'ticket_creation'),
    path('ticket_update/<int:ticket_id>/', ticket_update, name= 'ticket_update'),
    path('ticket_rebooking/<int:ticket_id>/', ticket_rebooking, name= 'ticket_rebooking'),

    path('ticket_upload/<int:ticket_id>/', ticket_upload, name= 'ticket_upload'),
    path('ticket_status_update/<int:ticket_id>/<str:new_status>/', ticket_status_update, name= 'ticket_status_update'),
    path('additional_creation/<int:ticket_id>/', additional_creation, name= 'additional_creation'),
    path('additional_remove/<int:additional_id>/', additional_remove, name= 'additional_remove'),
]