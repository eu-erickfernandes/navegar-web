import json
from datetime import datetime

from django.core.management.base import BaseCommand
from apps.authentication.models import CustomUser
from apps.route.models import Boat, City, RouteBoatWeekday
from apps.ticket.models import Ticket, Passenger, Cargo

class Command(BaseCommand):
    help = 'Initial data'

    def handle(self, *args, **kwargs):
        print('INITIAL TICKET DATA')

        new_passengers = 0
        new_cargos = 0
        new_tickets = 0

        try:
            ticket_file = open('backup/ticket_ticket.json', encoding= 'utf-8')
        except:
            print('CustomUser backup file not found')
            return
    
        ticket_data = json.load(ticket_file)

        for data in ticket_data['ticket_ticket']:
            created_at = datetime.fromisoformat(data['created_at'])

            if created_at.date().month >= 6 and data['status'] == 4:
                print('ADDING TICKET')
                print(f'CREATED AT {created_at}')

                origin_name = data['origin']
                destination_name = data['destination']

                print(f'{data["date"]}: {data["origin"]} - {data["destination"]}')

                user_create_id = data['user_create_id']

                date = data['date']

                boat_name = data['boat']

                cost = data['cost']
                value = data['value']

                if data['type'] == 'passageiro':
                    name_client = (data['name_client']).strip()
                    document_type = data['document_type']
                    document_client = data['document_client']
                    birth_date_client = data['birth_date_client']

                    try:
                        passenger = Passenger.objects.get(name= name_client)

                        if document_type == 'cpf':
                            passenger.cpf = document_client
                        else:
                            passenger.rg = document_client

                        passenger.birth_date = birth_date_client

                        passenger.save()
                    except:
                        print('ADDING PASSENGER')

                        passenger = Passenger.objects.create(
                            name= name_client,
                            birth_date= birth_date_client
                        )

                        if document_type == 'cpf':
                            passenger.cpf = document_client
                        else:
                            passenger.rg = document_client

                        passenger.save()

                        print(f'PASSENGER {passenger} CREATED')
                        new_passengers += 1

                    ticket = Ticket.objects.create(
                        created_at= created_at,
                        created_by= CustomUser.objects.get(id= user_create_id),

                        passenger= passenger,

                        boat= Boat.objects.get(name= boat_name),

                        origin= City.objects.get(name= origin_name),
                        destination= City.objects.get(name= destination_name),

                        date= date,

                        departure_time= RouteBoatWeekday.objects.get(id= data['route_weekday_id']).departure_time,
                        arrival_time= RouteBoatWeekday.objects.get(id= data['route_weekday_id']).arrival_time,
                        next_day= RouteBoatWeekday.objects.get(id= data['route_weekday_id']).next_day,

                        cost= cost,
                        price= value,

                        status= 'paid'
                    )

                    print(f'TICKET {ticket} CREATED')
                    new_tickets += 1

                else:
                    cargo_description = data['cargo_description']
                    cargo_weight = data['cargo_weight']

                    cargo = Cargo.objects.create(
                        description= cargo_description,
                        weight= cargo_weight
                    )

                    print(f'CARGO {cargo} CREATED')
                    new_cargos += 1

                    ticket = Ticket.objects.create(
                        created_at= created_at,
                        created_by= CustomUser.objects.get(id= user_create_id),

                        cargo= cargo,

                        boat= Boat.objects.get(name= boat_name),

                        origin= City.objects.get(name= origin_name),
                        destination= City.objects.get(name= destination_name),

                        date= date,

                        departure_time= RouteBoatWeekday.objects.get(id= data['route_weekday_id']).departure_time,
                        arrival_time= RouteBoatWeekday.objects.get(id= data['route_weekday_id']).arrival_time,
                        next_day= RouteBoatWeekday.objects.get(id= data['route_weekday_id']).next_day,

                        cost= cost,
                        price= value,

                        status= 'paid'
                    )

                    print(f'TICKET {ticket} CREATED')
                    new_tickets += 1

            print()

        print(f'NEW TICKETS: {new_tickets}')
        print(f'NEW PASSENGERS: {new_passengers}')
        print(f'NEW CARGOS: {new_cargos}')