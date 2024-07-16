from django.shortcuts import render, redirect
from django.urls import reverse

from apps.route.models import RouteBoatWeekday
from .models import Passenger, Ticket

# Create your views here.
def index(request):
    tickets = Ticket.objects.all().order_by('created_at')

    return render(request, 'ticket/index.html', {
        'tickets': tickets
    })

def add(request, route_boat_weekday_id, date):
    passengers = Passenger.objects.all().order_by('name')

    try:
        route_boat_weekday = RouteBoatWeekday.objects.get(id= route_boat_weekday_id)
    except:
        return redirect(reverse('route:search'))
    
    return render(request, 'ticket/add.html', {
        'boat': route_boat_weekday.boat,
        'hidden_navbar': True,
        'date': date,
        'passengers': passengers,
        'route': route_boat_weekday.route,
        'route_boat_weekday': route_boat_weekday
    })