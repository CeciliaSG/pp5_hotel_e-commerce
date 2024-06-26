from django import forms
from booking.models import SpaBooking


class SpaBookingForm(forms.ModelForm):
    """
    Form for creating or updating a spa booking.
    From Boutique Ado walkthrough.

    This form inherits from `forms.ModelForm`
    and is designed to handle data input
    related to spa bookings, including customer name,
    email, and phone number.

    Attributes:
        Meta:
            model (SpaBooking): The model class associated
            with this form.
            fields (list): The fields from the `SpaBooking`
            model to be included in the form.

    Methods:
        __init__(self, *args, **kwargs):
            Custom initialization method to set placeholders,
            autofocus, CSS classes, and labels for form fields
            dynamically.

    Usage:
        This form can be used in Django templates to render HTML
        forms for creating or updating spa bookings. It automatically
        sets placeholders with or without asterisks for required fields,
        applies a specific CSS class to form inputs, and autofocuses on
        the first input field.
    """

    class Meta:
        model = SpaBooking
        fields = ['customer_name', 'email',
                  'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'customer_name': 'Customer Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
        }

        self.fields['customer_name'].widget.attrs[
            'autofocus'] = True

        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
