from django.urls import path

from .views import *

app_name = 'finantial'

urlpatterns = [
    # VIEWS
    path('', dashboard, name= 'dashboard'),
]