from django.db import models

from apps.authentication.models import CustomUser
from apps.route.models import Boat, City

class Passenger(models.Model):
    name = models.CharField(max_length= 100)
    birth_date = models.DateField(null= True)
    cpf = models.CharField(max_length= 14, null= True)
    rg = models.CharField(max_length= 50, null= True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    created_at = models.DateTimeField(auto_now_add= True)
    created_by = models.ForeignKey(CustomUser, on_delete= models.PROTECT)
    passenger = models.ForeignKey(Passenger, on_delete= models.PROTECT, null= True)
    boat = models.ForeignKey(Boat, on_delete= models.PROTECT)

    origin = models.ForeignKey(City, on_delete= models.PROTECT, related_name= 'ticket_origin')
    destination = models.ForeignKey(City, on_delete= models.PROTECT, related_name= 'ticket_destination')

    date = models.DateField()

    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    next_day = models.BooleanField()

    cost = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    document = models.FileField(null= True)

    status = models.IntegerField(default= 1)


class TicketCargo(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete= models.PROTECT)

    description = models.CharField(max_length=100, null= True)
    weight = models.CharField(max_length=10, null= True)