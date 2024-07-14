from django.contrib import admin

from .models import City, Boat, Route, RouteBoat, RouteBoatWeekday

# Register your models here.
class BoatAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier')
    list_filter = ('name', 'supplier')
    search_fields = ('name', 'supplier')

admin.site.register(Boat, BoatAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'uf')
    list_filter = ('uf',)
    ordering = ('name',)
    search_fields = ('name',)

admin.site.register(City, CityAdmin)


class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination')

admin.site.register(Route, RouteAdmin)

class RouteBoatAdmin(admin.ModelAdmin):
    list_display = ('route', 'boat')

admin.site.register(RouteBoat, RouteBoatAdmin)

class RouteBoatWeekdayAdmin(admin.ModelAdmin):
    list_display = ('route_boat', 'weekday')

admin.site.register(RouteBoatWeekday, RouteBoatWeekdayAdmin)