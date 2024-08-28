from datetime import datetime

from django.utils import timezone

from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.ticket.models import Ticket, Additional

from .models import Observation

@require_POST
def ticket_check(request):
    for item in request.POST.items():
        if item[1] == 'on':
            ticket_id = item[0]

            try:
                ticket = Ticket.objects.get(id= ticket_id)
            except:
                return redirect(reverse('finantial:dashboard'))
            
            ticket.status = 'paid'
            ticket.save()

    return redirect(reverse('finantial:dashboard'))

@require_POST
def finantial_update(request):
    for item in request.POST.items():
        if 'ticket' in item[0]:
            print(item)
            ticket_id = item[0].split('_')[1]

            try:
                ticket = Ticket.objects.get(id= ticket_id)
            except:
                return redirect(reverse('finantial:index'))
            
            ticket.status = 'paid'
            ticket.paid_at = timezone.now()
            ticket.save()
        elif 'additional' in item[0]:
            print(item)
            additional_id = item[0].split('_')[1]

            try:
                additional = Additional.objects.get(id= additional_id)
            except:
                return redirect(reverse('finantial:index'))
            
            additional.status = 'paid'
            additional.paid_at = timezone.now()
            additional.save()
            
    return redirect(reverse('finantial:index'))

def finantial_update(post, id_tickets_list, date):
    for id in id_tickets_list:
        ticket = Ticket.objects.get(id= id)

        paid = False
        
        for item in post.items():
            if f'ticket_{id}' in item[0]:
                paid = True

        ticket.status = 'paid' if paid else 'pending'
        ticket.paid_at = timezone.now() if paid else None
        ticket.save()

        for additional in ticket.get_additional():
            paid = False

            for item in post.items():
                if f'additional_{additional.id}' in item[0]:
                    paid = True

            additional.status = 'paid' if paid else 'pending'
            additional.paid_at = timezone.now() if paid else None
            additional.save()


    observation_description = post.get('observation_description')

    observation = Observation.objects.get_or_create(date= date)[0]
    observation.description = observation_description

    observation.save()