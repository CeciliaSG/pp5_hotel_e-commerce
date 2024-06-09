from django.contrib import admin
from .models import SpaBooking, SpaBookingServices

# Register your models here.

class SpaBookingServicesAdminInline(admin.TabularInline):
    model = SpaBookingServices
    readonly_fields = ('spa_service_total',)


class SpaBookingAdmin(admin.ModelAdmin):

    inlines = (SpaBookingServicesAdminInline,)

    readonly_fields = ('booking_number', 'booking_date',
                        'booking_total', 'original_cart', 'stripe_pid',)

    fields = ('booking_number', 'customer_profile', 'booking_date', 'customer_name', 
                'email', 'phone_number', 'booking_total', 'original_cart', 'stripe_pid',)

    list_display = ('booking_number', 'booking_date', 'customer_name', 
                     'email', 'phone_number', 'date_and_time', 'booking_total',)
    
    #ordering = ('-booking_date',)
    
    list_filter = ('booking_date',)

admin.site.register(SpaBooking, SpaBookingAdmin)


class SpaBookingServicesAdmin(admin.ModelAdmin):
    list_display = ('spa_service', 'quantity', 'spa_service_total', 'spa_booking')
    list_filter = ('spa_booking__booking_date',)

admin.site.register(SpaBookingServices, SpaBookingServicesAdmin)