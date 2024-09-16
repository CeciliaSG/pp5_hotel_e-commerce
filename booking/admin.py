from django.contrib import admin
from .models import SpaBooking, SpaBookingServices

# Register your models here.


class SpaBookingServicesAdminInline(admin.TabularInline):
    """
    Inline admin configuration for SpaBookingServices model.

    Displays spa services related to a booking, with a readonly field for
    the total service cost. Allows adding additional services with the
    'extra' option.
    """
    model = SpaBookingServices
    readonly_fields = ('spa_service_total',)
    extra = 1


class SpaBookingAdmin(admin.ModelAdmin):
    """
    Admin configuration for SpaBooking model.

    - Inlines the SpaBookingServicesAdminInline to allow editing related
      services.
    - Sets readonly fields such as booking number, date, total, and payment
      details.
    - Specifies the fields to display in the admin form, including customer
      information and booking details.
    - Customizes the list display in the admin overview, showing key booking
      details.
    - Adds a filter for bookings by date.
    """
    inlines = (SpaBookingServicesAdminInline,)
    readonly_fields = (
        'booking_number', 'booking_date', 'booking_total',
        'original_cart', 'stripe_pid',
    )
    fields = (
        'booking_number', 'customer_profile', 'booking_date',
        'customer_name', 'email', 'phone_number', 'date_and_time',
        'booking_total', 'original_cart', 'stripe_pid',
    )
    list_display = (
        'booking_number', 'booking_date', 'customer_name', 'email',
        'phone_number', 'date_and_time', 'booking_total',
    )
    list_filter = ('booking_date',)


admin.site.register(SpaBooking, SpaBookingAdmin)


class SpaBookingServicesAdmin(admin.ModelAdmin):
    """
    Admin configuration for SpaBookingServices model.

    - Displays key fields such as spa service, quantity, total cost, and
      associated booking in the admin list view.
    - Adds a filter for bookings by booking date, allowing easy filtering
      of services by the associated booking date.
    - Enables search functionality for spa services by name and for bookings
      by customer name.
    """
    list_display = (
        'spa_service', 'quantity', 'spa_service_total', 'spa_booking',
    )
    list_filter = ('spa_booking__booking_date',)
    search_fields = (
        'spa_service__name', 'spa_booking__customer_name',
    )


admin.site.register(SpaBookingServices, SpaBookingServicesAdmin)