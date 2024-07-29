from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.ticket.models import Ticket

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