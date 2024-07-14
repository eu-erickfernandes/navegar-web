from django.contrib import admin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone')
    search_fields = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
