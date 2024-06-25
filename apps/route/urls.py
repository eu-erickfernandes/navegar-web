from django.urls import path

from apps.route.views import *

app_name = 'route'

urlpatterns = [
    path('', index, name= 'index')
]