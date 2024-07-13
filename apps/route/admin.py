from django.contrib import admin

from .models import City, Boat

# Register your models here.
class BoatAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier')
    list_filter = ('name', 'supplier')
    search_fields = ('name', 'supplier')

admin.site.register(Boat, BoatAdmin)

class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

admin.site.register(City, CityAdmin)