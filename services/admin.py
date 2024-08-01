from django.contrib import admin
from .models import (Availability, TimeSlotAvailability, 
SpaService, SpecificDate, TimeSlot, ServiceCategory)

# Inline for SpecificDate within AvailabilityAdmin
class SpecificDateInline(admin.TabularInline):
    model = Availability.specific_dates.through
    extra = 3
    can_delete = True
    verbose_name = "Specific Date"
    verbose_name_plural = "Specific Dates"


# Inline for TimeSlotAvailability within AvailabilityAdmin
class TimeSlotAvailabilityInline(admin.TabularInline):
    model = TimeSlotAvailability
    extra = 5
    fields = ['specific_date', 'time_slot', 'is_available']
    autocomplete_fields = ['time_slot']


class SpecificDateAdmin(admin.ModelAdmin):
    list_display = ("date",)

admin.site.register(SpecificDate, SpecificDateAdmin)


# Availability Admin
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("spa_service",)
    inlines = [TimeSlotAvailabilityInline]

admin.site.register(Availability, AvailabilityAdmin, )


# Register TimeSlot and SpaService separately
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('time',)
    list_filter = ('time', 'spa_service')
    search_fields = ['time']

admin.site.register(TimeSlot, TimeSlotAdmin)


class SpaServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "is_access")
    list_filter = ("category", "is_access")

admin.site.register(SpaService, SpaServiceAdmin)
