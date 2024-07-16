from django.contrib import admin

from .models import Ticket, Passenger, TicketCargo

# Register your models here.
class TicketAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'created_by', 'origin', 'destination', 'passenger')
    ordering = ('created_at',)

admin.site.register(Ticket, TicketAdmin)

class TicketCargoAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'description', 'weight')

admin.site.register(TicketCargo, TicketCargoAdmin)

class PassengerAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'rg', 'birth_date')

admin.site.register(Passenger, PassengerAdmin)