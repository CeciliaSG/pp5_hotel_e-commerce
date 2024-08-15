from django.contrib import admin
from .models import (Availability, TimeSlotAvailability, 
SpaService, SpecificDate, TimeSlot, ServiceCategory, Review)
from .forms import SpecificDateAdminForm


class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)

admin.site.register(ServiceCategory, ServiceCategoryAdmin)

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


#SpecificDateAdmin (Bulk add dates to chose from)
class SpecificDateAdmin(admin.ModelAdmin):
    form = SpecificDateAdminForm
    list_display = ("date",)

    def save_model(self, request, obj, form, change):

        dates = form.cleaned_data['dates']
        date_list = set([date.strip() for date in dates.split(',') if date.strip()])

        unique_dates = set(date_list)

        specific_date_objects = []
        for date in date_list:

            if not SpecificDate.objects.filter(date=date).exists():
                specific_date_objects.append(specific_date)

        SpecificDate.objects.bulk_create(specific_date_objects)

    def save_related(self, request, form, formsets, change):
        pass
  
admin.site.register(SpecificDate, SpecificDateAdmin)


# Availability Admin
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("spa_service",)
    inlines = [TimeSlotAvailabilityInline]

admin.site.register(Availability, AvailabilityAdmin, )


# TimeSlots 
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('time',)
    list_filter = ('time', 'spa_service')
    search_fields = ['time']

admin.site.register(TimeSlot, TimeSlotAdmin)

# SpaService
class SpaServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "is_access")
    list_filter = ("category", "is_access")

admin.site.register(SpaService, SpaServiceAdmin)

admin.site.register(Review)