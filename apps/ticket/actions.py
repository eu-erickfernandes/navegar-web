from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.route.models import RouteBoatWeekday
from .models import Ticket, Passenger, TicketCargo

from utils.format import date_format

@require_POST
def ticket_creation(request, route_boat_weekday_id, date):
    try:
        route_boat_weekday = RouteBoatWeekday.objects.get(id= route_boat_weekday_id)
    except:
        return redirect(f'/passagens/adicionar/{route_boat_weekday_id}/{date}/')
    
    created_by = request.user
    boat = route_boat_weekday.boat
    origin = route_boat_weekday.origin
    destination = route_boat_weekday.destination
    date = date
    departure_time = route_boat_weekday.departure_time
    arrival_time = route_boat_weekday.arrival_time
    next_day = route_boat_weekday.next_day
    cost = route_boat_weekday.cost
    price = route_boat_weekday.price

    ticket_type = request.POST.get('ticket_type')

    if ticket_type == 'passenger':
        for item in request.POST.items():
            print(item)
            if 'passenger_name' in item[0]:
                index = item[0].split('_')[2]
                
                name = item[1]

                passenger = Passenger.objects.create(
                    name= name
                )

                if request.POST.__contains__(f'passenger_cpf_{index}'):
                    cpf = request.POST.get(f'passenger_cpf_{index}')
                    passenger.cpf = cpf

                if request.POST.__contains__(f'passenger_birth_{index}'):
                    birth_date = request.POST.get(f'passenger_birth_{index}')
                    passenger.birth_date = date_format(birth_date)

                if request.POST.__contains__(f'passenger_rg_{index}'):
                    rg = request.POST.get(f'passenger_rg_{index}')
                    passenger.rg = rg

                passenger.save()

                Ticket.objects.create(
                    created_by= created_by,
                    passenger= passenger,
                    boat= boat,

                    origin= origin,
                    destination= destination,

                    date= date,

                    departure_time= departure_time,
                    arrival_time= arrival_time,
                    next_day= next_day,
                    
                    cost= cost,
                    price= price
                )

            if 'radio_passenger' in item[0]:
                index = item[0].split('_')[2]
                id = item[1]

                passenger = Passenger.objects.get(id= id)

                Ticket.objects.create(
                    created_by= created_by,
                    passenger= passenger,
                    boat= boat,

                    origin= origin,
                    destination= destination,

                    date= date,

                    departure_time= departure_time,
                    arrival_time= arrival_time,
                    next_day= next_day,
                    
                    cost= cost,
                    price= price
                )
    else:
        description = request.POST.get('description')
        weight = request.POST.get('weight')

        ticket = Ticket.objects.create(
            created_by= created_by,
            boat= boat,

            origin= origin,
            destination= destination,

            date= date,

            departure_time= departure_time,
            arrival_time= arrival_time,
            next_day= next_day,
            
            cost= cost,
            price= price
        )

        TicketCargo.objects.create(
            ticket= ticket,
            weight= weight,
            description= description
        )
    return redirect(reverse('ticket:index'))