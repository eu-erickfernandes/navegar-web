from django.contrib import admin

from .models import Ticket, Passenger, Cargo, Additional

# Register your models here.
class TicketAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'created_by', 'rebooking', 'no_show', 'status', 'origin', 'destination', 'passenger', 'cargo', 'price')

admin.site.register(Ticket, TicketAdmin)


class PassengerAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'rg', 'birth_date')

admin.site.register(Passenger, PassengerAdmin)


class CargoAdmin(admin.ModelAdmin):
    list_display = ('description', 'weight')

admin.site.register(Cargo, CargoAdmin)


class AdditionalAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'created_at', 'description', 'value', 'status', 'paid_at',)

admin.site.register(Additional, AdditionalAdmin)