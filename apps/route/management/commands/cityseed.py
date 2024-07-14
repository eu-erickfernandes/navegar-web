import requests
from django.core.management.base import BaseCommand
from apps.route.models import City


class Command(BaseCommand):
    help = 'Initial state of City Model'

    def handle(self, *args, **kwargs):
        print('INITIALIZING CITIES SEED')

        new_cities = 0

        initial_citys = requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/estados/13/municipios').json()

        for city in initial_citys:
            name = city.get('nome')
            uf = 'AM'
            print(f'ADDING "{name} - {uf}"')
            
            if City.objects.filter(name= name, uf= uf).exists():
                print(f'CITY "{name} - {uf}" ALREADY EXISTS')
                print()
                continue
            
            City.objects.create(
                name= name,
                uf= uf
            )
        
            new_cities += 1
            print(f'CITY "{name} - {uf}" CREATED')

            print()
            
        print(f'SEED FINISHED. {new_cities} CITIES CREATED.')