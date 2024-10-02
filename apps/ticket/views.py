from datetime import datetime

from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from xhtml2pdf import pisa

from apps.route.models import RouteBoatWeekday, Route, City
from .models import Passenger, Ticket, Cargo


@login_required
def index(request):
    tickets = Ticket.objects.all().order_by('-created_at')

    # ticket_test = tickets.first()

    # from .messages import ticket_creation_message

    # ticket_creation_message(request, ticket_test)

    # HANDLING THE ID SEARCH
    if request.GET.__contains__('id'):
        id = request.GET.get('id')
        tickets = tickets.filter(id= id)

        return render(request, 'ticket/index.html', {
            'id': id,
            'tickets': tickets
        })

    tickets_count = tickets.count()

    paginator = Paginator(tickets, 10)

    page_number = request.GET.get('page')
    tickets = paginator.get_page(page_number) 

    return render(request, 'ticket/index.html', {
        'tickets': tickets,
        'tickets_count': tickets_count,
        'paginator': paginator
    })


@login_required
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


@login_required
def ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id= ticket_id)
        ticket_cargo = None

        if not ticket.passenger:
            ticket_cargo = Cargo.objects.get(ticket= ticket)
    except:
        return redirect(reverse('ticket:index'))
    
    return render(request, 'ticket/ticket.html', {
        'hidden_navbar': True,
        'ticket': ticket,
        'ticket_cargo': ticket_cargo
    })


@login_required
def rebooking(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id= ticket_id)
    except:
        return redirect(reverse('ticket:index'))

    available_origins_ids = Route.objects.values_list('origin', flat= True)
    available_destinations_ids = Route.objects.values_list('destination', flat= True)

    origins = City.objects.filter(id__in= available_origins_ids)
    destinations = City.objects.filter(id__in= available_destinations_ids)

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

        return render(request, 'ticket/rebooking.html', {
            'date': date,
            'destination': destination,
            'destinations': destinations,
            'hidden_navbar': True,
            'origin': origin,
            'origins': origins,
            'route_boat_weekdays': route_boat_weekdays,
            'ticket': ticket,
        })

    return render(request, 'ticket/rebooking.html', {
        'destinations': destinations,
        'hidden_navbar': True,
        'origins': origins,
        'ticket': ticket
    })

# @login_required
def pdf(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id= ticket_id)
        ticket_cargo = None

        if not ticket.passenger:
            ticket_cargo = Cargo.objects.get(ticket= ticket)
    except:
        return redirect(reverse('ticket:index'))
    
    title = f'{ticket.boat} - { ticket.passenger.name if ticket.passenger else "CARGA" } - {ticket.date} - { ticket.origin } - { ticket.destination }'

    aggreko_logo_path = str(settings.BASE_DIR) + '/static/images/aggreko.png'
    cp_logo_path = str(settings.BASE_DIR) + '/static/images/cp.png'

    response = HttpResponse(pdf, content_type= 'application/pdf')
    response['Content-Disposition'] = f'filename={ title }.pdf'

    template = get_template('ticket/pdf.html')
    
    html = template.render({
        'aggreko_logo_path': aggreko_logo_path,
        'cp_logo_path': cp_logo_path,
        'ticket': ticket,
        'ticket_cargo': ticket_cargo,
        'title': title
    })

    pisaStatus = pisa.CreatePDF(html, dest= response, encoding=('utf-8'))

    if pisaStatus.err:
        return HttpResponse('Erros')
    return response