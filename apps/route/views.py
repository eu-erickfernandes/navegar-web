from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.authentication.decorators import required_user_roles
from .models import City, RouteBoatWeekday, Route, Boat

@login_required
@required_user_roles('A')
def index(request):
    routes = Route.objects.all()

    return render(request, 'route/index.html', {
        'routes': routes
    })

@login_required
def boats(request):
    boats = Boat.objects.all()

    return render(request, 'route/boats.html', {
        'boats': boats
    })

@login_required
def search(request):
    available_origins_ids = Route.objects.values_list('origin', flat= True)
    available_destinations_ids = Route.objects.values_list('destination', flat= True)

    origins = City.objects.filter(id__in= available_origins_ids)
    destinations = City.objects.filter(id__in= available_destinations_ids)

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
            'date': date,
            'destination': destination,
            'destinations': destinations,
            'origin': origin,
            'origins': origins,
            'route_boat_weekdays': route_boat_weekdays,
            'today': today
        })


    return render(request, 'route/search.html', {
        'destinations': destinations,
        'origins': origins,
        'today': today
    })