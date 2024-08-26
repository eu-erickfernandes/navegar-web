from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.route.models import RouteBoatWeekday
from .models import Ticket, Passenger, Cargo

from utils.format import date_format

from services.whatsapp_api import send_message

def new_ticket_message(request, ticket):
    description = ''
    
    date = f'{ticket.date.split("-")[2]}/{ticket.date.split("-")[1]}/{ticket.date.split("-")[0]}'
    pdf_path = f'http://{request.get_host()}/passagens/{ticket.id}/pdf'

    if ticket.passenger:
        description = f'Passageiro: {ticket.passenger.name}'

    if ticket.cargo:
        description = f'Carga: {ticket.cargo.description}'

    return f'{date} {ticket.origin} - {ticket.destination}\nSaída: {ticket.departure_time}\nChegada: {ticket.arrival_time}\nLancha: {ticket.boat}\nValor: {ticket.price}\n\n{description}\nVoucher: {pdf_path}'

@require_POST
def ticket_creation(request, route_boat_weekday_id, date):
    try:
        route_boat_weekday = RouteBoatWeekday.objects.get(id= route_boat_weekday_id)
    except:
        return redirect(f'/passagens/adicionar/{route_boat_weekday_id}/{date}/')
    print(request.POST)
    
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
    rebooking = request.POST.get('rebooking') != None
    no_show = request.POST.get('no_show') != None

    ticket_type = request.POST.get('ticket_type')

    if ticket_type == 'passenger':
        for item in request.POST.items():
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
                    passenger.birth_date = date_format(birth_date) or None

                if request.POST.__contains__(f'passenger_rg_{index}'):
                    rg = request.POST.get(f'passenger_rg_{index}')
                    passenger.rg = rg

                passenger.save()

                ticket = Ticket.objects.create(
                    created_by= created_by,
                    passenger= passenger,
                    boat= boat,

                    origin= origin,
                    destination= destination,

                    date= date,

                    departure_time= departure_time,
                    arrival_time= arrival_time,
                    next_day= next_day,
                    rebooking= rebooking,
                    no_show= no_show,
                    
                    cost= cost,
                    price= price,

                    status= 'analyzing' if request.POST.get('analyzing') != None else 'pending'
                )

                message = new_ticket_message(request, ticket)
                # response = send_message('556899546899', message)

            if 'radio_passenger' in item[0]:
                index = item[0].split('_')[2]
                id = item[1]

                passenger = Passenger.objects.get(id= id)

                ticket = Ticket.objects.create(
                    created_by= created_by,

                    boat= boat,

                    origin= origin,
                    destination= destination,

                    date= date,

                    departure_time= departure_time,
                    arrival_time= arrival_time,
                    next_day= next_day,
                    rebooking= rebooking,
                    no_show= no_show,
                    
                    cost= cost,
                    price= price,

                    passenger= passenger,

                    status= 'analyzing' if request.POST.get('analyzing') != None else 'pending'
                )

                message = new_ticket_message(request, ticket)
                # response = send_message('556899546899', message)

                
    else:
        description = request.POST.get('description')
        weight = request.POST.get('weight')

        cargo = Cargo.objects.create(
            description= description,
            weight= weight,
        )

        ticket = Ticket.objects.create(
            created_by= created_by,
            boat= boat,

            cargo= cargo,

            origin= origin,
            destination= destination,

            date= date,

            departure_time= departure_time,
            arrival_time= arrival_time,
            next_day= next_day,
            rebooking= rebooking,
            no_show= no_show,
            
            cost= cost,
            price= price,

            status= 'analyzing' if request.POST.get('analyzing') != None else 'pending'
        )
        
        message = new_ticket_message(request, ticket)
        # response = send_message('556899546899', message)
    return redirect(reverse('ticket:index'))


@require_POST
def ticket_upload(request, ticket_id):
    ticket = Ticket.objects.get(id= ticket_id)

    file = request.FILES.get('file')
    file.name = f'/ticket_{ticket.id}/{file.name}'
    ticket.file = file
    ticket.save()

    return redirect(f'/passagens/passagem/{ticket_id}/')


@require_POST
def ticket_status_update(request, ticket_id, new_status):
    ticket = Ticket.objects.get(id= ticket_id)

    ticket.status = new_status
    
    ticket.save()
    
    return redirect(f'/passagens/passagem/{ticket_id}/')


@require_POST
def ticket_no_show_toggle(request, ticket_id):
    ticket = Ticket.objects.get(id= ticket_id)

    ticket.no_show = True
    ticket.save()
    
    return redirect(f'/passagens/passagem/{ticket_id}/')