from django import forms
from booking.models import SpaBooking

class SpaBookingForm(forms.ModelForm):
    class Meta:
        model = SpaBooking
        fields = ['customer_name', 'email', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'customer_name': 'Customer Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
        }

        self.fields['customer_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False 

