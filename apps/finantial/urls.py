from django.urls import path

from .views import *
from .actions import *

app_name = 'finantial'

urlpatterns = [
    # VIEWS
    path('dashboard/', dashboard, name= 'dashboard'),
    path('', index, name= 'index'),
    
    #ACTIONS
    path('finantial_update/', finantial_update, name= 'finantial_update'),
    path('ticket_check/', ticket_check, name= 'ticket_check'),
]