from django import forms
from .models import SpaBooking, SpaBookingServices

class SpaBookingForm(forms.ModelForm):
    class Meta:
        model = SpaBooking
        fields = ['customer_name', 'email', 'phone_number', 'date_and_time']

class SpaBookingServicesForm(forms.ModelForm):
    class Meta:
        model = SpaBookingServices
        fields = ['spa_service', 'quantity']
