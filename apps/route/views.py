from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from apps.authentication.models import CustomUser
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
@required_user_roles('A')
def add(request):
    cities = City.objects.all()
    boats = Boat.objects.all()

    weekdays = [
        ('7', 'Domingo'),
        ('1', 'Segunda-Feira'),
        ('2', 'Terça-Feira'),
        ('3', 'Quarta-Feira'),
        ('4', 'Quinta-Feira'),
        ('5', 'Sexta-Feira'),
        ('6', 'Sábado'),
    ]

    return render(request, 'route/add.html', {
        'boats': boats,
        'cities': cities,
        'hidden_navbar': True,
        'weekdays': weekdays
    })


@login_required
@required_user_roles('A')
def route(request, route_id):
    try:
        route = Route.objects.get(id= route_id)
    except:
        raise Http404
    
    cities = City.objects.all()
    boats = Boat.objects.all()

    weekdays = [
        ('7', 'Domingo'),
        ('1', 'Segunda-Feira'),
        ('2', 'Terça-Feira'),
        ('3', 'Quarta-Feira'),
        ('4', 'Quinta-Feira'),
        ('5', 'Sexta-Feira'),
        ('6', 'Sábado'),
    ]

    return render(request, 'route/route.html', {
        'boats': boats,
        'cities': cities,
        'hidden_navbar': True,
        'route': route,
        'weekdays': weekdays
    })


@login_required
@required_user_roles('A')
def boats(request):
    suppliers = CustomUser.objects.filter(is_superuser= False, role='S').order_by('name')
    boats = Boat.objects.all()

    return render(request, 'route/boats.html', {
        'boats': boats,
        'suppliers': suppliers,
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

        # if(str(date) == str(today)):
        #     route_boat_weekdays = route_boat_weekdays.filter(
        #         route_boat__route__departure_time__gt= datetime.now().time()
        #     )

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