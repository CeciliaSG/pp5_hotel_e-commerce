from django import forms
from .models import SpaBooking, SpaBookingServices
from django.forms import inlineformset_factory


class SpaBookingForm(forms.ModelForm):
    class Meta:
        model = SpaBooking
        fields = ['customer_name', 'email', 'phone_number', 'date_and_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_and_time'].widget = forms.DateTimeInput(attrs={
            'class': 'formInputs',
            'placeholder': 'Select date and time',
            'type': 'datetime-local'
        })

class SpaBookingServicesForm(forms.ModelForm):
    class Meta:
        model = SpaBookingServices
        fields = ['spa_service', 'quantity']

SpaBookingServicesFormSet = inlineformset_factory(
    SpaBooking, SpaBookingServices, form=SpaBookingServicesForm, extra=1, can_delete=True
)