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
    list_display = ("time",)
    extra = 1


admin.site.register(TimeSlot, TimeSlotAdmin)


class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("spa_service",)


admin.site.register(Availability, AvailabilityAdmin)
