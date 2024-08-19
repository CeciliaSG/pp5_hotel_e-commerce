from django.contrib import admin
from django import forms 
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
    #verbose_name = "Specific Date"
    #verbose_name_plural = "Specific Dates"
    raw_id_fields = ['specific_date',]


# Inline for TimeSlotAvailability within AvailabilityAdmin
class TimeSlotAvailabilityInline(admin.TabularInline):
    model = TimeSlotAvailability
    extra = 5
    fields = ['specific_date', 'time_slot', 'is_available',]
    #autocomplete_fields = ['specific_date', 'time_slot',]

    
#SpecificDateAdmin (Bulk add dates to chose from)
class SpecificDateAdmin(admin.ModelAdmin):
    form = SpecificDateAdminForm
    list_display = ("date",)
    search_fields = ['date']

    def save_model(self, request, obj, form, change):
        form.save(commit=True)

    def save_related(self, request, form, formsets, change):
        pass
  
admin.site.register(SpecificDate, SpecificDateAdmin)


# Availability Admin
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("spa_service",)
    inlines = [TimeSlotAvailabilityInline]
    raw_id_fields = ['spa_service',]

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
    search_fields = ['name']

admin.site.register(SpaService, SpaServiceAdmin)

admin.site.register(Review)