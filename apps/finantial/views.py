from datetime import datetime
from decimal import Decimal

from django.db.models.aggregates import Sum
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.ticket.models import Ticket

@login_required
def dashboard(request):
    main_date = datetime.now().date()
    last_month = main_date
    first_month = Ticket.objects.all().last().created_at.date()

    # HANDLING THE ROUTE SEARCH
    if request.GET.__contains__('month'):
        searched_month = request.GET.get('month')
        main_date = datetime(int(searched_month.split('-')[0]), int(searched_month.split('-')[1]), 1)

    tickets = Ticket.objects.filter(created_at__year= main_date.year, created_at__month= main_date.month)
    
    if tickets.count() > 0:
        total_invoicing = round(tickets.aggregate(Sum('price')).get('price__sum'), 2)
        total_cost = round(tickets.aggregate(Sum('cost')).get('cost__sum'), 2)
        total_profit = round(total_invoicing - total_cost, 2)
        
        try:
            total_paid = round(tickets.filter(status= 'paid').aggregate(Sum('price')).get('price__sum'), 2)
        except:
            total_paid = Decimal(0.0)
        
        try:
            total_pending = round(tickets.filter(status= 'pending').aggregate(Sum('price')).get('price__sum'), 2)
        except:
            total_pending = Decimal(0.0)

        total_profit = round(total_paid * Decimal(0.08), 2)

        days_list = tickets.dates('created_at', 'day', order= 'DESC')

        days = []

        for day in days_list:
            day_tickets = tickets.filter(created_at__day= day.day)

            day_total_cost = round(day_tickets.aggregate(Sum('cost')).get('cost__sum'), 2)
            day_total_invoicing = round(day_tickets.aggregate(Sum('price')).get('price__sum'), 2)
            day_total_profit = round(day_total_invoicing - day_total_cost, 2)

            try:
                day_total_pending = round(day_tickets.filter(status= 'pending').aggregate(Sum('price')).get('price__sum'), 2)
            except:
                day_total_pending = Decimal(0.0)

            try:
                day_total_paid = round(day_tickets.filter(status= 'paid').aggregate(Sum('price')).get('price__sum'), 2)
            except:
                day_total_paid = Decimal(0.0)

            day_total_profit = round(day_total_paid * Decimal(0.08), 2)

            days.append(
                {
                    'day': day,
                    'total_cost': day_total_cost,
                    'total_invoicing': day_total_invoicing,
                    'total_profit': day_total_profit,
                    'total_paid': day_total_paid,
                    'total_pending': day_total_pending,
                    'tickets': tickets.filter(created_at__day= day.day)
                }
            )
    else:
        return render(request, 'finantial/dashboard.html', {

        })

    return render(request, 'finantial/dashboard.html', {
        'days': days,
        'first_month': first_month,
        'last_month': last_month,
        'main_date': main_date,
        'total_cost': total_cost,
        'total_invoicing': total_invoicing,
        'total_paid': total_paid,
        'total_pending': total_pending,
        'total_profit': total_profit,
        'tickets': tickets,
    })