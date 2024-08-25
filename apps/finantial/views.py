from datetime import datetime
from decimal import Decimal

from django.db.models.aggregates import Sum
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.ticket.models import Ticket
from apps.route.models import PROFIT_MARGIN


@login_required
def dashboard(request):
    main_date = datetime.now().date()
    last_month = main_date

    # HANDLING THE ROUTE SEARCH
    if request.GET.__contains__('month'):
        searched_month = request.GET.get('month')
        main_date = datetime(int(searched_month.split('-')[0]), int(searched_month.split('-')[1]), 1)

    tickets = Ticket.objects.filter(created_at__year= main_date.year, created_at__month= main_date.month).exclude(status__in= ['analyzing', 'cancelled'])

    days = []

    total_paid = Decimal(0.0)
    total_pending = Decimal(0.0)

    if tickets.count() > 0:
        for ticket in tickets:
            if ticket.status == 'paid' or ticket.status == 'completed':
                total_paid += ticket.value
            elif ticket.status == 'pending':
                total_pending += ticket.value

    # total_paid = round(tickets.filter(status= 'paid').aggregate(Sum('price')).get('price__sum'), 2) if tickets.filter(status= 'paid').count() > 0 else Decimal(0.0)
    total_profit = round(total_paid * PROFIT_MARGIN, 2) 

    # total_pending = round(tickets.filter(status= 'pending').aggregate(Sum('price')).get('price__sum'), 2) if tickets.filter(status= 'pending').count() > 0 else Decimal(0.0)
    total_pending_profit = round(total_pending * PROFIT_MARGIN, 2) 
    
    if tickets.count() > 0:
        days_list = tickets.dates('created_at', 'day', order= 'DESC')

        for day in days_list:
            day_tickets = tickets.filter(created_at__day= day.day)

            # try:
            #     day_total_pending = round(day_tickets.filter(status= 'pending').aggregate(Sum('price')).get('price__sum'), 2)
            # except:
            #     day_total_pending = Decimal(0.0)


            # try:
            #     day_total_paid = round(day_tickets.filter(status= 'paid').aggregate(Sum('price')).get('price__sum'), 2)
            # except:
            #     day_total_paid = Decimal(0.0)

            day_total_paid = Decimal(0.0)
            day_total_pending = Decimal(0.0)

            if day_tickets.count() > 0:
                for ticket in day_tickets:
                    if ticket.status == 'paid' or ticket.status == 'completed':
                        day_total_paid += ticket.value
                    elif ticket.status == 'pending':
                        day_total_pending += ticket.value

            day_total_profit = round(day_total_paid * PROFIT_MARGIN, 2)
            day_total_pending_profit = round(day_total_pending * PROFIT_MARGIN, 2)

            days.append(
                {
                    'day': day,
                    'total_profit': day_total_profit,
                    'total_paid': day_total_paid,
                    'total_pending': day_total_pending,
                    'total_pending_profit': day_total_pending_profit,
                    'tickets': tickets.filter(created_at__day= day.day)
                }
            )

    return render(request, 'finantial/dashboard.html', {
        'days': days,
        'last_month': last_month,
        'main_date': main_date,
        'total_paid': total_paid,
        'total_pending': total_pending,
        'total_pending_profit': total_pending_profit,
        'total_profit': total_profit,
        'tickets': tickets,
    })