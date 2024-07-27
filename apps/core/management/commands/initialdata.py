import json

from django.core.management.base import BaseCommand
from apps.authentication.models import CustomUser
from apps.route.models import City, Boat, Route, RouteBoat, RouteBoatWeekday


class Command(BaseCommand):
    help = 'Initial data'

    def handle(self, *args, **kwargs):
        print('INITIAL APP DATA')

        new_users = 0
        
        new_cities = 0
        new_boats = 0
        new_routes = 0
        new_route_boats = 0
        new_route_boat_weekdays = 0

        # USER DATA
        try:
            custom_user_file = open('backup/user_customuser.json', encoding= 'utf-8')
        except:
            print('CustomUser backup file not found')
            return
    
        custom_user_data = json.load(custom_user_file)

        for data in custom_user_data['user_customuser']:
            print('ADDING USER')
            print(data["full_name"])
            
            id = data["id"]
            name = data["full_name"]
            email = data["email"]
            phone = data["phone"]
            password = data["password"]
            role = 'S' if data['type'] == 'F' else 'A'

            try:
                user = CustomUser.objects.create(
                    id= id,
                    name= name,
                    email= email,
                    phone= phone,
                    password= password,
                    role= role
                )

                print(f'USER {user} CREATED')
                new_users += 1
            except:
                print('ERROR')
            
            print()
            

        # CITY DATA
        try:
            city_file = open('backup/route_location.json', encoding= 'utf-8')
        except:
            print('City backup file not found')
            return
        
        city_data = json.load(city_file)

        for data in city_data['route_location']:
            print('ADDING CITY')
            print(data['name'])

            id = data['id']
            name = data['name']

            try:
                city = City.objects.create(
                    id= id,
                    name= name,
                    uf= 'AM'
                )

                print(f'CITY {city} CREATED')
                new_cities += 1
            except:
                print('ERROR')

            print()

        
        # BOAT DATA
        try:
            boat_file = open('backup/route_boat.json', encoding= 'utf-8')
        except:
            print('Boat backup file not found')
            return
        
        boat_data = json.load(boat_file)

        for data in boat_data['route_boat']:
            print('ADDING BOAT')
            print(data['name'])
            
            id = data['id']
            name = data['name']
            supplier_id = data['supplier_id']

            try:
                supplier = CustomUser.objects.get(id= supplier_id)

                boat = Boat.objects.create(
                    id= id,
                    name= name,
                    supplier= supplier
                )

                print(f'BOAT {boat} CREATED')
                new_boats += 1
            except:
                print('ERROR')

            print()

        
        # ROUTE DATA
        try:
            route_file = open('backup/route_route.json', encoding= 'utf-8')
        except:
            print('Route backup file not found')
            return
        
        route_data = json.load(route_file)

        for data in route_data['route_route']:
            print('ADDING ROUTE')

            id = data['id']
            origin_id = data['origin_id']
            destination_id = data['destination_id']

            try:
                origin = City.objects.get(id= origin_id)
                destination = City.objects.get(id= destination_id)

                print(f'{origin} - {destination}')

                departure_time = data['departure_time']
                arrival_time = data['arrival_time']
                next_day = bool(data['after_midnight'])

                cost = data['cost']
                price = data['value']

                route = Route.objects.create(
                    id= id,
                    origin= origin,
                    destination= destination,
                    departure_time= departure_time,
                    arrival_time= arrival_time,
                    next_day= next_day,
                    cost= cost,
                    price= price
                )

                print(f'ROUTE {route} CREATED')
                new_routes += 1
            except:
                print('ERROR')

            print()

        
        # ROUTE_BOAT AND ROUTE_WEEKDAY DATA
        try:
            route_weekday_file = open('backup/route_routeweekday.json', encoding= 'utf-8')
        except:
            print('Route backup file not found')
            return
        
        route_weekday_data = json.load(route_weekday_file)

        weekday_dict = {
            'Monday': '1',
            'Tuesday': '2',
            'Wednesday': '3',
            'Thursday': '4',
            'Friday': '5',
            'Saturday': '6',
            'Sunday': '7',
        }

        for data in route_weekday_data['route_routeweekday']:
            print('ADDING ROUTE WEEKDAY')

            id = data['id']
            
            route_id = data['route_id']
            boat_id = data['boat_id']

            try:
                route = Route.objects.get(id= route_id)
                boat = Boat.objects.get(id= boat_id)
                weekday = data['weekday']

                print(f'{route} - {boat} - {weekday}')

                try:
                    route_boat = RouteBoat.objects.get(route= route, boat= boat)
                except:
                    print('ADDING ROUTE BOAT')
                    print(f'{route} - {boat}')

                    route_boat = RouteBoat.objects.create(
                        route= route,
                        boat= boat
                    )

                    print(f'ROUTE BOAT {route_boat} CREATED')
                    new_route_boats += 1
                
                if not RouteBoatWeekday.objects.filter(route_boat= route_boat, weekday= weekday_dict[weekday]):
                    route_boat_weekday = RouteBoatWeekday.objects.create(
                        id= id,
                        route_boat= route_boat,
                        weekday = weekday_dict[weekday]
                    )

                    print(f'{route_boat_weekday.id} - ROUTE BOAT WEEKDAY {route_boat_weekday} CREATED')
                    new_route_boat_weekdays += 1
                else:
                    print('ERROR')
            except:
                print('ERROR')

            print()
            

        print(f'NEW USERS: {new_users}')

        print(f'NEW CITIES: {new_cities}')
        print(f'NEW BOATS: {new_boats}')
        print(f'NEW ROUTES: {new_routes}')
        print(f'NEW ROUTE_BOATS: {new_route_boats}')
        print(f'NEW ROUTE_BOAT_WEEKDAYS: {new_route_boat_weekdays}')