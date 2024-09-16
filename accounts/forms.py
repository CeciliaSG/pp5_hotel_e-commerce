from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from .models import CustomerProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }

        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = \
                placeholders.get(field, field.capitalize())
            self.fields[field].widget.attrs['class'] = \
                'border-black-rounded-o customer-profile-form-input'
            self.fields[field].label = False

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class CustomerProfileForm(forms.ModelForm):
    """
    Form for updating or creating a CustomerProfile
    instance.

    This form allows users to provide or update
    the following fields:
    - Default Phone Number (required)
    - Date of Birth
    - City

    The `__init__` method customizes the form fields by:
    1. Setting placeholder text for each field.
    2. Removing the labels for a cleaner form appearance.
    3. Enforcing that the 'default_phone_number' field is required.

    The placeholders and styling help improve the user experience
    when filling out the form.
    """
    class Meta:
        model = CustomerProfile
        fields = ['default_phone_number', 'date_of_birth', 'city']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'date_of_birth': 'Date of Birth as: YYYY/DD/MM',
            'city': 'City',
        }

        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = \
                placeholders.get(field, field.capitalize())
            self.fields[field].widget.attrs['class'] = \
                'border-black-rounded-o customer-profile-form-input'
            self.fields[field].label = False

        self.fields['default_phone_number'].required = True


class CustomSignupForm(SignupForm):
    """
    Custom signup form that extends the default allauth
    SignupForm to collect additional user information
    during registration.

    This form collects the following additional fields:
    - First Name (required)
    - Last Name (required)
    - Phone Number (required)
    - Date of Birth (optional)
    - City (optional)

    The save method overrides the default save behavior to:
    1. Save the first name and last name to the user instance.
    2. Create a CustomerProfile instance with the phone number,
    date of birth, city, and other related fields.

    This ensures that the User and associated CustomerProfile
    are created and populated with the custom data provided
    during signup.
    """
    first_name = forms.CharField(
        max_length=30, label='First Name', required=True
    )
    last_name = forms.CharField(
        max_length=30, label='Last Name', required=True
    )
    phone_number = forms.CharField(
        max_length=20, label='Phone Number', required=True
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date'
        }),
        required=False,
        label='Date of Birth (optional)'
    )
    city = forms.CharField(
        max_length=100, label='City (optional)', required=False
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        date_of_birth = self.cleaned_data.get('date_of_birth', None)
        city = self.cleaned_data.get('city', None)

        CustomerProfile.objects.create(
            user=user,
            default_phone_number=self.cleaned_data['phone_number'],
            email=user.email,
            date_of_birth=date_of_birth,
            city=city
        )
        return user


class DeleteAccountForm(forms.Form):
    """
    Form class for users to delete their
    account and all associated information
    """
    confirm_delete = forms.BooleanField(
        required=True, label='Confirm Account Deletion'
    )
