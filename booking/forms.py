from django import forms
from booking.models import SpaService
from django.forms import formset_factory


class ServiceBookingForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=SpaService.objects.all(), empty_label="Select a service"
    )
    date_and_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control",
                "placeholder": "Select date and time",
                "type": "datetime-local",
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


ServiceBookingFormSet = formset_factory(ServiceBookingForm, extra=1)
