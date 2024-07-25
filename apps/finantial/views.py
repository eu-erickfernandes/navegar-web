from django.shortcuts import render

from apps.ticket.models import Ticket

# Create your views here.
def dashboard(request):
    tickets = Ticket.objects.all()

    return render(request, 'finantial/dashboard.html', {
        'tickets': tickets,
    })