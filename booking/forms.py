from django import forms
from .models import SpaBooking
from services.models import SpaService, TimeSlot

class DateInput(forms.DateInput):
    input_type = 'date'

class ServiceBookingForm(forms.ModelForm):
    class Meta:
        model = SpaBooking
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
        queryset=SpaService.objects.all(), empty_label="Select a service",
        widget=forms.Select(attrs={"class": "form-control service-select"})
    )
    date = forms.DateField(
        widget=DateInput(
            attrs={
                'type': 'date',
                "class": "form-control",
                "placeholder": "Select date",
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

class TimeSlotSelectionForm(forms.Form):
    selected_time_slot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.all(), empty_label=None, widget=forms.RadioSelect
    )
    def __str__(self):
        return "TimeSlotSelectionForm"
