from datetime import datetime, timedelta
from decimal import Decimal

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.authentication.models import CustomUser
from apps.ticket.models import Ticket, Additional
from .models import PROFIT_MARGIN

from .models import Observation 
from .actions import finantial_update 

@login_required
def index(request):
    main_date = datetime.now().date()

    suppliers = CustomUser.objects.filter(role= 'S')

    # HANDLING THE DATE FILTER SUBMIT
    if request.GET.__contains__('date'):
        searched_date = request.GET.get('date').split('-')
        main_date = datetime(int(searched_date[0]), int(searched_date[1]), int(searched_date[2])).date()
    
    # previous_date = main_date - timedelta(days= 1)
    previous_date = main_date
    
    # HANDLING THE SUPPLIER FILTER SUBMIT
    searched_supplier = CustomUser.objects.get(id= request.GET.get('supplier')) if request.GET.__contains__('supplier') and request.user.role == 'A' else None

    if searched_supplier:
        pending_tickets = Ticket.objects.filter(status= 'pending', created_at__date__lt= previous_date, boat__supplier= searched_supplier)
        paid_tickets = Ticket.objects.filter(status= 'paid', paid_at__date= main_date, boat__supplier= searched_supplier)
        previous_tickets = Ticket.objects.filter(created_at__date= previous_date, status= 'pending', boat__supplier= searched_supplier)

        pending_additionals = Additional.objects.filter(status= 'pending', created_at__date__lt= previous_date, ticket__boat__supplier= searched_supplier)
        paid_additionals = Additional.objects.filter(status= 'paid', paid_at__date= main_date, ticket__boat__supplier= searched_supplier)
        previous_additionals = Additional.objects.filter(created_at__date= previous_date, status= 'pending', ticket__boat__supplier= searched_supplier)
    else:
        pending_tickets = Ticket.objects.filter(status= 'pending', created_at__date__lt= previous_date)
        paid_tickets = Ticket.objects.filter(status= 'paid', paid_at__date= main_date)
        previous_tickets = Ticket.objects.filter(created_at__date= previous_date, status= 'pending')

        pending_additionals = Additional.objects.filter(status= 'pending', created_at__date__lt= previous_date)
        paid_additionals = Additional.objects.filter(status= 'paid', paid_at__date= main_date)
        previous_additionals = Additional.objects.filter(created_at__date= previous_date, status= 'pending')

    tickets = pending_tickets.union(previous_tickets).union(paid_tickets)
    additionals = pending_additionals.union(previous_additionals).union(paid_additionals)

    if request.POST:
        id_tickets_list = tickets.values_list('id', flat= True)
        id_additionals_list = additionals.values_list('id', flat= True)

        finantial_update(request.POST, id_tickets_list, id_additionals_list, main_date)

    tickets = tickets.order_by('created_at')

    observation = Observation.objects.get(date= main_date) if Observation.objects.filter(date= main_date).exists() else None

    total = Decimal(0.0)
    total_paid = Decimal(0.0)
    total_pending = Decimal(0.0)

    if tickets.count() > 0:
        for ticket in tickets:
            total += ticket.price

            if ticket.status in ['paid', 'completed']:
                total_paid += ticket.price
            elif ticket.status == 'pending':
                total_pending += ticket.price 

        for additional in additionals:
            total += additional.value

            if additional.status == 'paid':
                total_paid += additional.value
            elif additional.status == 'pending':
                total_pending += additional.value
 
    total_profit = round(total_paid * PROFIT_MARGIN, 2) 
    total_pending_profit = round(total_pending * PROFIT_MARGIN, 2) 

    customer_total = total_pending + total_pending_profit

    return render(request, 'finantial/index.html', {
        'additionals': additionals,
        'customer_total': customer_total,
        'tickets': tickets,
        'total': total,
        'total_paid': total_paid,
        'total_pending': total_pending,
        'total_pending_profit': total_pending_profit,
        'total_profit': total_profit,
        'main_date': main_date,
        'observation': observation,
        'searched_supplier': searched_supplier,
        'suppliers': suppliers,
    })

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
                total_paid += ticket.price
            elif ticket.status == 'pending':
                total_pending += ticket.price

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
                        day_total_paid += ticket.price
                    elif ticket.status == 'pending':
                        day_total_pending += ticket.price

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