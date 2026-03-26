from django.contrib import admin

# Register your models here.
from .models import User, CountryCode

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_staff','country_code_id')
    search_fields = ('username', 'email', 'phone_number','country_code_id')

@admin.register(CountryCode)
class CountryCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'country_name')
    search_fields = ('code', 'country_name')
