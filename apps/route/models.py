from django.db import models


from apps.authentication.models import CustomUser

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return self.name
    

class Boat(models.Model):
    supplier = models.ForeignKey(CustomUser, on_delete= models.PROTECT)

    name = models.CharField(max_length= 100)

    def __str__(self):
        return self.name
    

class Route(models.Model):
    origin = models.ForeignKey(City, on_delete= models.PROTECT, related_name= 'origin')
    destination = models.ForeignKey(City, on_delete= models.PROTECT, related_name= 'destination')

    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    next_day = models.BooleanField()

    cost = models.DecimalField(max_digits= 10, decimal_places= 2) 
    price = models.DecimalField(max_digits= 10, decimal_places= 2)

    def __str__(self):
        return f'{self.origin} - {self.destination}'


class RouteBoat(models.Model):
    route = models.ForeignKey(Route, on_delete= models.PROTECT)
    boat = models.ForeignKey(Boat, on_delete= models.PROTECT)

    def __str__(self):
        return f'{self.route} - {self.boat}'


class RouteBoatWeekday(models.Model):
    WEEKDAY_CHOICES = [
        ('1', 'Domingo'),
        ('2', 'Segunda-Feira'),
        ('3', 'Terça-Feira'),
        ('4', 'Quarta-Feira'),
        ('5', 'Quinta-Feira'),
        ('6', 'Sexta-Feira'),
        ('7', 'Sábado'),
    ]

    route_boat = models.ForeignKey(RouteBoat, on_delete= models.PROTECT)
    weekday = models.CharField(max_length= 1, choices= WEEKDAY_CHOICES)