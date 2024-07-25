from django.core.management.base import BaseCommand
from apps.authentication.models import CustomUser
from apps.route.models import City, Boat, Route, RouteBoat, RouteBoatWeekday, RouteDiscount
from apps.ticket.models import Ticket, Cargo, Passenger


class Command(BaseCommand):
    help = 'Clear current data'

    def handle(self, *args, **kwargs):
        print('CLEANING CURRENT DATA')

        print(f'TICKETS: {Ticket.objects.all().count()}')
        Ticket.objects.all().delete()

        print(f'CARGOS: {Cargo.objects.all().count()}')
        Cargo.objects.all().delete()

        print(f'PASSENGERS: {Passenger.objects.all().count()}')
        Passenger.objects.all().delete()

        print(f'ROUTE_BOAT_WEEKDAYS: {RouteBoatWeekday.objects.all().count()}')
        RouteBoatWeekday.objects.all().delete()

        print(f'ROUTE_BOATS: {RouteBoat.objects.all().count()}')
        RouteBoat.objects.all().delete()

        print(f'ROUTES: {Route.objects.all().count()}')
        Route.objects.all().delete()

        print(f'BOATS: {Boat.objects.all().count()}')
        Boat.objects.all().delete()

        print(f'CITYS: {City.objects.all().count()}')
        City.objects.all().delete()

        print(f'CUSTOM_USERS: {CustomUser.objects.all().exclude(is_superuser= True).count()}')
        CustomUser.objects.all().exclude(is_superuser= True).delete()
