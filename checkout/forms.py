from django import forms
from booking.models import SpaBooking

class SpaBookingForm(forms.ModelForm):
    class Meta:
        model = SpaBooking
        fields = ['customer_name', 'email', 'phone_number', 'date_and_time']

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        placeholders = {
        'customer_name': 'Customer Name',
        'email': 'Email Address',
        'phone_number': 'Phone Number',
        }

        self.fields["date_and_time"].widget = forms.DateTimeInput(
            attrs={
                "class": "formInputs",
                "placeholder": "Select date and time",
                "type": "datetime-local",
            }
        )
