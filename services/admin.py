from django.contrib import admin
from .models import Availability, TimeSlotAvailability, SpaService, SpecificDate, TimeSlot, ServiceCategory

# Register Time Slot
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('time',)
    search_fields = ['time']  # Allow searching by the 'time' field

admin.site.register(TimeSlot, TimeSlotAdmin)

# Register Specific Date
class SpecificDateAdmin(admin.ModelAdmin):
    list_display = ("date",)

admin.site.register(SpecificDate, SpecificDateAdmin)

# Inline for TimeSlotAvailability within AvailabilityAdmin
class TimeSlotAvailabilityInline(admin.TabularInline):
    model = TimeSlotAvailability
    extra = 3  # Number of empty forms to display for adding new time slots
    fields = ['specific_date', 'time_slot', 'is_available']
    autocomplete_fields = ['time_slot']  # Enable autocomplete for time_slot

# Availability Admin
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("spa_service",)
    inlines = [TimeSlotAvailabilityInline]

admin.site.register(Availability, AvailabilityAdmin)

# Register TimeSlotAvailability separately as well
class TimeSlotAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('time_slot', 'specific_date', 'is_available')
    list_filter = ('specific_date', 'is_available')
    actions = ['mark_available', 'mark_unavailable']

    def mark_available(self, request, queryset):
        queryset.update(is_available=True)
        self.message_user(request, "Selected time slots have been marked as available.")
    mark_available.short_description = "Mark selected time slots as available"

    def mark_unavailable(self, request, queryset):
        queryset.update(is_available=False)
        self.message_user(request, "Selected time slots have been marked as unavailable.")
    mark_unavailable.short_description = "Mark selected time slots as unavailable"

admin.site.register(TimeSlotAvailability, TimeSlotAvailabilityAdmin)