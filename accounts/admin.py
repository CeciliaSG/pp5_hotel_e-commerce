from django.contrib import admin
from .models import CustomerProfile

# Register your models here.

class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_email', 'default_phone_number')

admin.site.register(CustomerProfile, CustomerProfileAdmin)