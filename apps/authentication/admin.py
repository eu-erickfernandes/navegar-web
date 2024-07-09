from django.contrib import admin
from .models import CustomUser, Person

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('person', 'email', 'phone')
    search_fields = ('email',)
    ordering = ('person',)

admin.site.register(CustomUser, CustomUserAdmin)


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'birth_date')
    ordering = ('name',)

admin.site.register(Person, PersonAdmin)