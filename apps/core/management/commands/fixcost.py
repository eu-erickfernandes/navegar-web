from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.route.models import Route
from apps.ticket.models import Ticket


class Command(BaseCommand):
    help = 'Clear current data'

    def handle(self, *args, **kwargs):
        print('FIXING COST VALUES')

        routes = Route.objects.all()

        for route in routes:
            print(f'ROUTE: {route}')
            print(f'PRICE: {route.price}')
            print(f'COST: {route.cost}')

            fixed_cost = route.price * Decimal('0.92')

            print(f'FIXED COST: {route.price} x .92 = {fixed_cost}')

            route.cost = fixed_cost
            route.save()

            print(f'COST FIXED TO {route.cost}')

            print()

        tickets = Ticket.objects.all()

        for ticket in tickets:
            print(f'TICEKT: {ticket}')
            print(f'PRICE: {ticket.price}')
            print(f'COST: {ticket.cost}')

            fixed_cost = ticket.price * Decimal('0.92')

            print(f'FIXED COST: {ticket.price} x .92 = {fixed_cost}')

            ticket.cost = round(fixed_cost, 2)
            ticket.save()

            print(f'COST FIXED TO {ticket.cost}')

            print()