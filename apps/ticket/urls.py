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
    path('ticket_upload/<int:ticket_id>/', ticket_upload, name= 'ticket_upload'),
    path('ticket_status_update/<int:ticket_id>/<str:new_status>/', ticket_status_update, name= 'ticket_status_update'),
    path('ticket_no_show_toggle/<int:ticket_id>/', ticket_no_show_toggle, name= 'ticket_no_show_toggle'),
]