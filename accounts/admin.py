from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import CustomerProfile

# Register your models here.


class CustomerProfileInline(admin.StackedInline):
    """
    Inline admin descriptor for CustomerProfile model.
    Adds a CustomerProfile section to the User admin page.
    Prevents deletion of CustomerProfile instances.
    """
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = 'Customer Profiles'


class UserAdmin(BaseUserAdmin):
    """
    Custom admin for the User model that includes
    the CustomerProfile inline.

    This admin class adds the CustomerProfile inline to
    the standard User admin
    page, allowing management of CustomerProfile data
    alongside User data.

    The `get_inline_instances` method ensures that the inline
    form is only
    displayed when editing an existing User instance
    (i.e., not during creation).
    """
    inlines = (CustomerProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)

admin.site.register(User, UserAdmin)
