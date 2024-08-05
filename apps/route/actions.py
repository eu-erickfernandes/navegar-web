from decimal import Decimal

from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from .models import Route, RouteBoat, Boat, RouteBoatWeekday, City

@require_POST
def route_creation(request):
    origin = request.POST.get('origin')
    destination = request.POST.get('destination')

    departure_time = request.POST.get('departure_time')
    arrival_time = request.POST.get('arrival_time')

    next_day = request.POST.get('next_day') != None

    price = Decimal(request.POST.get('price').replace(',', '.'))

    route = Route.objects.create(
        origin= City.objects.get(id= origin),
        destination= City.objects.get(id= destination),
        departure_time= departure_time,
        arrival_time= arrival_time,
        next_day= next_day,
        price= price,
        cost= price
    )

    for item in request.POST.items():
        if 'boat' in item[0]:
            index = item[0].split('-')[1]
            
            boat_id = item[1]
            boat = Boat.objects.get(id= boat_id)

            route_boat = RouteBoat.objects.create(
                route= route,
                boat= boat
            )

            for post_item in request.POST.items():
                if not 'route_boat' in post_item[0] and f'{index}-weekday' in post_item[0]:
                    weekday = post_item[0].split('-')[2]

                    route_boat_weekday = RouteBoatWeekday.objects.create(
                        route_boat= route_boat,
                        weekday= weekday
                    )


    return redirect(f'/rotas/{route.id}')


@require_POST
def route_update(request, route_id):
    route = Route.objects.get(id= route_id)

    origin = request.POST.get('origin')
    destination = request.POST.get('destination')

    departure_time = request.POST.get('departure_time')
    arrival_time = request.POST.get('arrival_time')

    next_day = request.POST.get('next_day') != None

    price = Decimal(request.POST.get('price').replace(',', '.'))

    route.origin = City.objects.get(id= origin)
    route.destination = City.objects.get(id= destination)
    route.departure_time = departure_time
    route.arrival_time = arrival_time
    route.next_day = next_day
    route.price = price

    route.save()

    route_boats = []
    route_boat_weekdays = []

    for item in request.POST.items():
        if 'route_boat' in item[0]:
            route_boat_id = item[0].split('-')[1]
            route_boat = RouteBoat.objects.get(id= route_boat_id)

            if '-boat' in item[0]:
                boat_id = item[1]
                boat = Boat.objects.get(id= boat_id)

                route_boat.boat = boat
                route_boat.save()

                route_boats.append(route_boat.id)
            elif '-weekday' in item[0]:
                weekday = item[0].split('-')[3]

                route_boat_weekday = RouteBoatWeekday.objects.get_or_create(
                    route_boat= route_boat,
                    weekday= weekday
                )

                route_boat_weekdays.append(route_boat_weekday[0].id)

        elif 'boat' in item[0]:
            index = item[0].split('-')[1]
            
            boat_id = item[1]
            boat = Boat.objects.get(id= boat_id)

            route_boat = RouteBoat.objects.get_or_create(
                route= route,
                boat= boat
            )

            route_boats.append(route_boat[0].id)

            for post_item in request.POST.items():
                if not 'route_boat' in post_item[0] and f'{index}-weekday' in post_item[0]:
                    weekday = post_item[0].split('-')[2]

                    route_boat_weekday = RouteBoatWeekday.objects.get_or_create(
                        route_boat= route_boat[0],
                        weekday= weekday
                    )

                    route_boat_weekdays.append(route_boat_weekday[0].id)

    RouteBoatWeekday.objects.filter(route_boat__route= route).exclude(id__in= route_boat_weekdays).delete()
    RouteBoat.objects.filter(route= route).exclude(id__in= route_boats).delete()

    return redirect(f'/rotas/{route_id}')