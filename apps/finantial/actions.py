from django.utils import timezone

from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.ticket.models import Ticket, Additional

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