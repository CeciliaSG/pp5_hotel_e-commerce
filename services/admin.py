from django.contrib import admin
from django import forms
from .models import (Availability, TimeSlotAvailability,
SpaService, SpecificDate, TimeSlot, ServiceCategory, Review)
from .forms import SpecificDateAdminForm, TimeSlotAvailabilityForm

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
    raw_id_fields = ['specific_date',]

    def clean(self):
        super().clean()
        seen_dates = set()
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                specific_date = form.cleaned_data.get('specificdate')
                
                if specific_date in seen_dates:
                    raise ValidationError(f"The date {specific_date} is already associated with this availability.")
                
                if self.instance.specific_dates.filter(id=specific_date.id).exists():
                    raise ValidationError(f"The date {specific_date} is already associated with this availability.")
                
                seen_dates.add(specific_date)


# Inline for TimeSlotAvailability within AvailabilityAdmin
class TimeSlotAvailabilityInline(admin.TabularInline):
    model = TimeSlotAvailability
    form = TimeSlotAvailabilityForm
    extra = 1
    fields = ['specific_date', 'time_slot', 'is_available', 'is_booked']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('specific_date__date', 'time_slot__time')

    def get_formset(self, request, obj=None, **kwargs):
        spa_service = obj.spa_service if obj else None

        formset_class = super().get_formset(request, obj, **kwargs)

        class CustomFormset(formset_class):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                for form in self.forms:
                    form.fields['time_slot'].queryset = TimeSlot.objects.filter(spa_service=spa_service)

        return CustomFormset


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
    raw_id_fields = ['spa_service']

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj=obj)
        return inline_instances

admin.site.register(Availability, AvailabilityAdmin)


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