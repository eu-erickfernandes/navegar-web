from datetime import datetime
from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.utils import timezone

from apps.authentication.models import CustomUser
from apps.route.models import Boat, City

class Passenger(models.Model):
    name = models.CharField(max_length= 100)
    birth_date = models.DateField(null= True)
    cpf = models.CharField(max_length= 14, null= True)
    rg = models.CharField(max_length= 50, null= True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
    

class Cargo(models.Model):
    description = models.CharField(max_length=100, null= True)
    weight = models.CharField(max_length=10, null= True)

    def __str__(self):
        return f'{self.description} - {self.weight}'
    
    class Meta:
        ordering = ['description']

class Ticket(models.Model):
    STATUS_CHOICES= [
        ('analyzing', 'Em Análise'),
        ('cancelled', 'Cancelado'),
        ('completed', 'Finalizado '),
        ('paid', 'Pago'),
        ('pending', 'Pendente'),
    ]

    created_at = models.DateTimeField(auto_now_add= True)
    created_by = models.ForeignKey(CustomUser, on_delete= models.PROTECT)

    passenger = models.ForeignKey(Passenger, on_delete= models.PROTECT, null= True, blank= True)
    cargo = models.ForeignKey(Cargo, on_delete= models.PROTECT, null= True, blank= True)

    boat = models.ForeignKey(Boat, on_delete= models.PROTECT)

    origin = models.ForeignKey(City, on_delete= models.PROTECT, related_name= "ticket_origin")
    destination = models.ForeignKey(City, on_delete= models.PROTECT, related_name= "ticket_destination")

    date = models.DateField()

    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    next_day = models.BooleanField()

    cost = models.DecimalField(max_digits= 10, decimal_places= 2)
    price = models.DecimalField(max_digits= 10, decimal_places= 2)

    file = models.FileField(upload_to= 'ticket_files/', blank= True, null= True)

    status = models.CharField(max_length= 20, choices= STATUS_CHOICES, default= 'pending')

    rebooking = models.BooleanField(default= False)
    no_show = models.BooleanField(default= False)

    paid_at = models.DateTimeField(default= None, null= True, blank= True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.date}: {self.origin} - {self.destination} - {"PASSENGER" if self.passenger else "CARGO"} - CREATED AT {self.created_at}'
    
    @property
    def arrival_date(self):
        return self.date + timedelta(days=1) if self.next_day else self.date

    def set_status(self, status):
        if status == 'paid':
            self.paid_at = timezone.now()
        elif status != 'completed':
            self.paid_at = None
        
        self.status = status
        self.save()
            
    def get_additional(self):
        return Additional.objects.filter(ticket= self)
            
    
class Additional(models.Model):
    STATUS_CHOICES= [
        ('paid', 'Pago'),
        ('pending', 'Pendente'),
    ]

    ticket = models.ForeignKey(Ticket, on_delete= models.PROTECT)
    created_at = models.DateTimeField(auto_now_add= True)

    description = models.CharField(max_length=100, null= True)
    value = models.DecimalField(max_digits= 10, decimal_places= 2)

    status = models.CharField(max_length= 20, choices= STATUS_CHOICES, default= 'pending')
    paid_at = models.DateTimeField(default= None, null= True, blank= True)

    def __str__(self):
        return f'{self.description} - {self.value} - CREATED AT {self.created_at}'