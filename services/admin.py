from django import forms
from django.contrib import admin

from .forms import SpecificDateAdminForm
from .forms import TimeSlotAvailabilityForm

from .models import Availability
from .models import TimeSlotAvailability
from .models import SpaService
from .models import SpecificDate
from .models import TimeSlot
from .models import ServiceCategory
from .models import Review


class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)


admin.site.register(ServiceCategory, ServiceCategoryAdmin)


class SpecificDateInline(admin.TabularInline):
    model = Availability.specific_dates.through
    extra = 3
    can_delete = True
    verbose_name = "Specific Date"
    verbose_name_plural = "Specific Dates"
    raw_id_fields = ['specific_date']

    def clean(self):
        super().clean()
        seen_dates = set()
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get(
                'DELETE', False
            ):
                specific_date = form.cleaned_data.get('specificdate')

                if specific_date in seen_dates:
                    raise ValidationError(
                        f"The date {specific_date} is already "
                        "associated with this availability."
                    )

                if self.instance.specific_dates.filter(
                    id=specific_date.id
                ).exists():
                    raise ValidationError(
                        f"The date {specific_date} is already "
                        "associated with this availability."
                    )

                seen_dates.add(specific_date)


class TimeSlotAvailabilityInline(admin.TabularInline):
    model = TimeSlotAvailability
    #form = TimeSlotAvailabilityForm
    extra = 1
    fields = ['specific_date', 'time_slot', 'is_available', 'is_booked']
    autocomplete_fields = ['specific_date', 'time_slot']

    def get_queryset(self, request):
        """
        Optimized queryset without slicing and raw ID fields.
        """
        qs = super().get_queryset(request)
        return qs.select_related('specific_date', 'time_slot')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "time_slot" and hasattr(self, 'spa_service'):
            kwargs["queryset"] = TimeSlot.objects.filter(spa_service=self.spa_service).order_by('time')
        elif db_field.name == "specific_date":
            kwargs["queryset"] = SpecificDate.objects.all().order_by('date')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        self.spa_service = obj.spa_service if obj else None
        return super().get_formset(request, obj, **kwargs)


class SpecificDateAdmin(admin.ModelAdmin):
    form = SpecificDateAdminForm
    list_display = ("date",)
    search_fields = ['date']

    def save_model(self, request, obj, form, change):
        form.save(commit=True)

    def save_related(self, request, form, formsets, change):
        pass


admin.site.register(SpecificDate, SpecificDateAdmin)


class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("spa_service",)
    inlines = [TimeSlotAvailabilityInline]
    list_select_related = ("spa_service",)

    def specific_dates_display(self, obj):
        """
        Custom display for specific dates in the list view.
        Prepares dates as comma-separated strings to avoid multiple DB queries.
        """
        return ", ".join([str(date) for date in obj.specific_dates.all()])

    def time_slots_display(self, obj):
        """
        Custom display for time slots in the list view.
        Retrieves related time slots efficiently.
        """
        return ", ".join([str(slot) for slot in obj.time_slots.all()])

    specific_dates_display.short_description = 'Specific Dates'
    time_slots_display.short_description = 'Time Slots'

    def get_queryset(self, request):
        """
        Optimized queryset that prefetches related data.
        This reduces the number of DB hits by fetching related specific dates and time slots.
        """
        queryset = super().get_queryset(request)
        return (
            queryset
            .select_related('spa_service')
            .prefetch_related('specific_dates')
            .prefetch_related('time_slots')
        )


admin.site.register(Availability, AvailabilityAdmin)


class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('time',)
    list_filter = ('time', 'spa_service')
    search_fields = ['time']


admin.site.register(TimeSlot, TimeSlotAdmin)


class SpaServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name", "price", "category", "is_access"
    )
    list_filter = ("category", "is_access")
    search_fields = ['name']


admin.site.register(SpaService, SpaServiceAdmin)


admin.site.register(Review)
