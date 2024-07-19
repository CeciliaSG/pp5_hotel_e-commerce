from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from .models import CustomerProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
        }
        
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = placeholders.get(field, field.capitalize())
            self.fields[field].widget.attrs['class'] = 'border-black-rounded-o customer-profile-form-input'
            self.fields[field].label = False


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['default_phone_number',]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
        }
        
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = placeholders.get(field, field.capitalize())
            self.fields[field].widget.attrs['class'] = 'border-black-rounded-o customer-profile-form-input'
            self.fields[field].label = False



class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=True)
    phone_number = forms.CharField(max_length=20, label='Phone Number', required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        """CustomerProfile.objects.create(
            user=user,
            default_phone_number=self.cleaned_data['phone_number'],
            email=user.email
        )"""
        return user
