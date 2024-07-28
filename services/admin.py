from django.contrib import admin
from .models import ServiceCategory, SpaService, SpecificDate
from .models import TimeSlot, Availability


class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

admin.site.register(ServiceCategory, ServiceCategoryAdmin)

class SpaServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "is_access")
    list_filter = ("category", "is_access")

admin.site.register(SpaService, SpaServiceAdmin)

class SpecificDateAdmin(admin.ModelAdmin):
    list_display = ("date",)

admin.site.register(SpecificDate, SpecificDateAdmin)

class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("time", "spa_service", "is_available")
    list_filter = ("spa_service", "is_available")
    actions = ['make_available', 'make_unavailable']

    def make_available(self, request, queryset):
        for slot in queryset:
            slot.is_available = True
            slot.save()
    make_available.short_description = "Mark selected time slots as available"

    def make_unavailable(self, request, queryset):
        for slot in queryset:
            slot.is_available = False
            slot.save()
    make_unavailable.short_description = "Mark selected time slots as unavailable"

admin.site.register(TimeSlot, TimeSlotAdmin)


class SpecificDateInline(admin.TabularInline):
    model = Availability.specific_dates.through
    extra = 1

class TimeSlotInline(admin.TabularInline):
    model = Availability.time_slots.through
    extra = 1

class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("spa_service",)
    inlines = [SpecificDateInline, TimeSlotInline]
    actions = ['make_time_slots_available']

    def make_time_slots_available(self, request, queryset):
        for availability in queryset:
            for time_slot in availability.time_slots.all():
                time_slot.is_available = True
                time_slot.save()
    make_time_slots_available.short_description = "Mark all time slots as available for selected availabilities"

admin.site.register(Availability, AvailabilityAdmin)