from django.urls import path

from .views import *
from .actions import *

app_name = 'finantial'

urlpatterns = [
    # VIEWS
    path('', dashboard, name= 'dashboard'),
    path('ticket_check/', ticket_check, name= 'ticket_check')
]