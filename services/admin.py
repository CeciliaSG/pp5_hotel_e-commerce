from django.contrib import admin
from .models import SpaService, ServiceCategory


# Register your models here.

class ServiceCategoryAdmin(admin.ModelAdmin):
   list_display = ('name',)

admin.site.register(ServiceCategory, ServiceCategoryAdmin)   


class SpaServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_access', 'available')
    list_filter = ('category', 'is_access', 'available')

admin.site.register(SpaService, SpaServiceAdmin)
