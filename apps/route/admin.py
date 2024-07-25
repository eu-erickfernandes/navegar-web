from django.contrib import admin

from .models import City, Boat, Route, RouteBoat, RouteBoatWeekday

# Register your models here.
class BoatAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier')
    list_filter = ('supplier',)
    search_fields = ('name',)

admin.site.register(Boat, BoatAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'uf')
    list_filter = ('uf',)
    search_fields = ('name',)

admin.site.register(City, CityAdmin)


class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'departure_time', 'arrival_time', 'next_day', 'cost', 'price')
    list_filter = ('origin', 'destination')

admin.site.register(Route, RouteAdmin)


class RouteBoatAdmin(admin.ModelAdmin):
    list_display = ('route', 'boat')
    list_filter = ('route', 'boat')

admin.site.register(RouteBoat, RouteBoatAdmin)


class RouteBoatWeekdayAdmin(admin.ModelAdmin):
    list_display = ('route_boat', 'weekday')
    list_filter = ('route_boat', 'weekday')

admin.site.register(RouteBoatWeekday, RouteBoatWeekdayAdmin)