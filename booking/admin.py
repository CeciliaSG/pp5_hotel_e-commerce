from django.contrib import admin
from .models import SpaBooking, SpaBookingServices

# Register your models here.

class SpaBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_number', 'customer_name', 'email', 'phone_number', 'booking_date', 'booking_total')
    list_filter = ('booking_date',)

admin.site.register(SpaBooking, SpaBookingAdmin)

class SpaBookingServicesAdmin(admin.ModelAdmin):
    list_display = ('spa_service', 'quantity', 'spa_service_total', 'spa_booking')
    list_filter = ('spa_booking__booking_date',)

admin.site.register(SpaBookingServices, SpaBookingServicesAdmin)