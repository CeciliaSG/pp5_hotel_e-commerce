from django import forms
from django.forms import fields
from django.forms.widgets import DateInput
from services.models import SpaService, TimeSlot


class ServiceBookingForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=SpaService.objects.all(), empty_label="Select a service"
    )
    date = forms.DateField(
        widget=DateInput(
            attrs={
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