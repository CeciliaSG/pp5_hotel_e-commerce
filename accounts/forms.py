from django import forms
from .models import CustomerProfile


class CustomerProfileForm(forms.ModelForm):
    """
    Form for updating customer profile information.

    This form inherits from `forms.ModelForm` and is
    used to update fields such as email
    and default phone number in the `CustomerProfile`
    model.

    Attributes:
        Meta:
            model (CustomerProfile): The model class associated
            with this form. fields (list): The fields from the
            `CustomerProfile` model to be included in the form.

    Methods:
        __init__(self, *args, **kwargs):
            Custom initialization method to set placeholders,
            autofocus, CSS classes, and labels for form fields
            dynamically.

    Usage:
        This form can be used in Django templates to render HTML
        forms for updating customer profile information. It automatically
        sets placeholders with or without asterisks for required fields,
        applies specific CSS classes to form inputs, and hides labels to
        provide a streamlined user interface for profile updates.
    """
    class Meta:
        model = CustomerProfile
        fields = ['email', 'default_phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'email': 'Email Address',
            'default_phone_number': 'Phone Number',
        }

        self.fields['email'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = \
                'border-black-rounded-o customer-profile-form-input'
            self.fields[field].label = False
