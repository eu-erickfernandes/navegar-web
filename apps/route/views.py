from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import City, RouteBoatWeekday, Route

@login_required
def index(request):
    routes = Route.objects.all()

    return render(request, 'route/index.html', {
        'routes': routes
    })

@login_required
def boats(request):
    return render(request, 'route/boats.html')

@login_required
def search(request):
    cities = City.objects.all()
    today = datetime.now().date()   

    # HANDLING THE ROUTE SEARCH
    if request.GET.get('origin') and request.GET.get('destination') and request.GET.get('date'):
        origin = City.objects.get(id= request.GET.get('origin'))
        destination = City.objects.get(id= request.GET.get('destination'))
        date = request.GET.get('date')
        
        splited_date = date.split('-')
        weekday = datetime(int(splited_date[0]), int(splited_date[1]), int(splited_date[2])).isoweekday()

        route_boat_weekdays = RouteBoatWeekday.objects.filter(
            route_boat__route__origin= origin, 
            route_boat__route__destination= destination, 
            weekday= weekday
        )

        if(str(date) == str(today)):
            route_boat_weekdays = route_boat_weekdays.filter(
                route_boat__route__departure_time__gt= datetime.now().time()
            )

        return render(request, 'route/search.html', {
            'cities': cities,
            'date': date,
            'destination': destination,
            'origin': origin,
            'route_boat_weekdays': route_boat_weekdays,
            'today': today
        })


    return render(request, 'route/search.html', {
        'cities': cities,
        'today': today
    })