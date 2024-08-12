from django import forms
from django.db import models

from .models import SpaBooking, SpaBookingServices
from services.models import SpaService, TimeSlot


class DateInput(forms.DateInput):
    """
    Widget class for rendering a date input field in a Django form.

    This widget extends `forms.DateInput` and sets the HTML input 
    type to 'date'. It is used to render date input fields in HTML
    forms with native date picker support in browsers that support it.

    Attributes:
        input_type (str): The type of input rendered by this widget,
        set to 'date' to ensure the browser displays a date picker
        for date inputs.

    Methods:
        None

    Usage:
        This widget is typically used as the `widgets` attribute in
        a Django form field definition, especially when defining
        forms that require date inputs. It ensures consistent
        rendering of date input fields across different browsers
        that support HTML5 date inputs.
    """
    input_type = 'date'


class ServiceBookingForm(forms.ModelForm):
    """
    Form for booking spa services with additional customisation 
    for fields.

    This form inherits from `forms.ModelForm` and is designed 
    for creating or updating spa bookings with fields such as
    service selection, date, and quantity.

    Attributes:
        Meta:
            model (SpaBooking): The model class associated with
            this form. fields (list): The fields from the `SpaBooking` 
            model to be included in the form. widgets (dict): 
            Custom widgets for specific fields (`date` and `quantity`)
            to control their appearance and behavior in HTML forms.

    Methods:
        None

    Usage:
        This form can be used in Django templates to render HTML forms
        for booking spa services. It provides customised widgets for the
        `date` and `quantity` fields, ensuring they are displayed with
        appropriate placeholders, CSS classes, and validation rules.
    """
    class Meta:
        model = SpaBookingServices
        fields = ['service', 'date', 'quantity']
        widgets = {
            'date': DateInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Select date",
                    "required": True
                }
            ),
            'quantity': forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Quantity"}
            ),
        }
    service = forms.ModelChoiceField(
        queryset=SpaService.objects.filter(status=1),
        empty_label="Select a service",
        widget=forms.Select(attrs={"class": "form-control service-select"})
    )  
    date = forms.DateField(
        widget=DateInput(
            attrs={
                'type': 'date',
                "class": "form-control",
                "required": True
            }
        )
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Quantity"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super(ServiceBookingForm, self).__init__(*args, **kwargs)

        if 'service' in self.data:
            service_id = self.data.get('service')
            service = SpaService.objects.get(id=service_id)

            if not service.is_access:
                self.fields['quantity'].widget = forms.HiddenInput()
        elif self.instance and hasattr(self.instance, 'service'):
            service = self.instance.service
            if not service.is_access:
                self.fields['quantity'].widget = forms.HiddenInput()


class TimeSlotSelectionForm(forms.Form):
    """
    Form for selecting a time slot from available options.

    This form allows users to select a time slot from a list
    of available options retrieved from the `TimeSlot` model.

    Attributes:
        selected_time_slot (forms.ModelChoiceField):
        A choice field representing the
        selected time slot, displayed
        using radio buttons.

    Methods:
        __str__(self):
            Returns a string representation of the form's name.

    Usage:
        This form is typically used in Django views and templates
        to render a list of available time slots for users to choose
        from using radio buttons.
    """
    selected_time_slot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.all(),
        empty_label=None, widget=forms.RadioSelect
    )

    def __str__(self):
        return "TimeSlotSelectionForm"
