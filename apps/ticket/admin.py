from django.contrib import admin

from .models import Ticket, Passenger, Cargo

# Register your models here.
class TicketAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'created_by', 'origin', 'destination', 'passenger', 'cargo')

admin.site.register(Ticket, TicketAdmin)


class PassengerAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'rg', 'birth_date')

admin.site.register(Passenger, PassengerAdmin)


class CargoAdmin(admin.ModelAdmin):
    list_display = ('description', 'weight')

admin.site.register(Cargo, CargoAdmin)