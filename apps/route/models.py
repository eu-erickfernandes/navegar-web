from datetime import datetime, timedelta

from django.db import models
from decimal import Decimal

from apps.authentication.models import CustomUser

PROFIT_MARGIN = Decimal(0.08)

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Boat(models.Model):
    supplier = models.ForeignKey(CustomUser, on_delete= models.PROTECT)
    name = models.CharField(max_length= 100)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
    

class Route(models.Model):
    origin = models.ForeignKey(City, on_delete= models.PROTECT, related_name= 'route_origin')
    destination = models.ForeignKey(City, on_delete= models.PROTECT, related_name= 'route_destination')

    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    next_day = models.BooleanField()

    cost = models.DecimalField(max_digits= 10, decimal_places= 2) 
    price = models.DecimalField(max_digits= 10, decimal_places= 2)

    def __str__(self):
        return f'{self.origin} - {self.destination}'
    
    class Meta:
        ordering = ['origin', 'destination']

    @property
    def profit(self):
        return round(self.price * PROFIT_MARGIN, 2)
    
    @property
    def duration(self):
        start_datetime = datetime.combine(datetime.today(), self.departure_time)
        end_datetime = datetime.combine(datetime.today(), self.arrival_time)

        if self.next_day:
            end_datetime += timedelta(days=1)

        total_time = end_datetime - start_datetime
        total_seconds = total_time.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        # minutes, seconds = divmod(remainder, 60)
        total_time = f"{int(hours):02}"

        return total_time
    
    @property
    def route_boats(self):
        return RouteBoat.objects.filter(route= self)


class RouteBoat(models.Model):
    route = models.ForeignKey(Route, on_delete= models.PROTECT)
    boat = models.ForeignKey(Boat, on_delete= models.PROTECT)

    def __str__(self):
        return f'{self.route} - {self.boat}'
    
    @property
    def route_boat_weekdays(self):
        return RouteBoatWeekday.objects.filter(route_boat= self)
    
    def weekdays_list(self):
        return list(RouteBoatWeekday.objects.filter(route_boat= self).values_list('weekday', flat= True))
    
    class Meta:
        ordering = ['route', 'boat']


class RouteBoatWeekday(models.Model):
    WEEKDAY_CHOICES = [
        ('1', 'Segunda-Feira'),
        ('2', 'Terça-Feira'),
        ('3', 'Quarta-Feira'),
        ('4', 'Quinta-Feira'),
        ('5', 'Sexta-Feira'),
        ('6', 'Sábado'),
        ('7', 'Domingo'),
    ]

    route_boat = models.ForeignKey(RouteBoat, on_delete= models.PROTECT)
    weekday = models.CharField(max_length= 1, choices= WEEKDAY_CHOICES)

    def __str__(self):
        return f'{self.route_boat} - {self.get_weekday_display()}'

    @property
    def boat(self):
        return self.route_boat.boat
    
    @property
    def route(self):
        return self.route_boat.route

    @property
    def origin(self):
        return self.route.origin

    @property
    def destination(self):
        return self.route.destination

    @property
    def departure_time(self):
        return self.route.departure_time

    @property
    def arrival_time(self):
        return self.route.arrival_time

    @property
    def next_day(self):
        return self.route.next_day
    
    @property
    def duration(self):
        return self.route.duration

    @property
    def cost(self):
        return self.route.cost
    
    @property
    def price(self):
        return self.route.price
    
    class Meta:
        ordering = ['route_boat', 'weekday']
    
class RouteDiscount(models.Model):
    supplier = models.ForeignKey(CustomUser, on_delete= models.PROTECT)
    route = models.ForeignKey(Route, on_delete= models.PROTECT)
    discounted_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discounted_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default= False)