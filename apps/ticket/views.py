from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings

from xhtml2pdf import pisa

from apps.route.models import RouteBoatWeekday
from .models import Passenger, Ticket, TicketCargo

def index(request):
    tickets = Ticket.objects.all().order_by('-created_at')

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



def pdf(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id= ticket_id)
        ticket_cargo = None

        if not ticket.passenger:
            ticket_cargo = TicketCargo.objects.get(ticket= ticket)
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