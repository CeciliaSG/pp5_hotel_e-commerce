from django import forms
from django.db import transaction
from django.forms.models import BaseInlineFormSet

from .models import (
    Review, SpaService, SpecificDate, TimeSlot,
    TimeSlotAvailability, Availability
)


class reviewForm(forms.ModelForm):
    """ Lets users review spa services. From Blog walkthrough """
    class Meta:
        model = Review
        fields = ('body',)


class MultiDateInput(forms.TextInput):
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control',
            'placeholder': 'Select multiple dates'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class SpecificDateAdminForm(forms.ModelForm):
    dates = forms.CharField(
        widget=MultiDateInput(attrs={'id': 'specific_dates_picker'}),
        help_text=(
            'Enter multiple dates separated by commas '
            '(e.g., 2024-08-01, 2024-08-02)'
        )
    )

    class Meta:
        model = SpecificDate
        fields = []

    def clean_dates(self):
        dates = self.cleaned_data['dates']
        date_list = [
            date.strip() for date in dates.split(',')
            if date.strip()
        ]

        if len(date_list) != len(set(date_list)):
            raise forms.ValidationError("You have entered duplicate dates.")

        existing_dates = (
            SpecificDate.objects.filter(date__in=date_list)
            .values_list('date', flat=True)
        )

        if existing_dates:
            formatted_dates = (
                date.strftime('%Y-%m-%d') for date in existing_dates
            )
            existing_dates_str = ", ".join(formatted_dates)
            error_message = (
                f"The following dates already exist: {existing_dates_str}"
            )
            raise forms.ValidationError(error_message)

        return date_list

    def save(self, commit=True):
        date_list = self.cleaned_data['dates']
        specific_date_objects = []
        for date in date_list:
            specific_date = SpecificDate(date=date)
            specific_date_objects.append(specific_date)
        if commit:
            SpecificDate.objects.bulk_create(specific_date_objects)
        return specific_date_objects

    class Media:
        js = (
            'https://cdn.jsdelivr.net/npm/flatpickr',
            'admin/js/init_flatpickr.js'
        )
        css = {
            'all': (
                'https://cdn.jsdelivr.net/npm/flatpickr/dist/'
                'flatpickr.min.css',
            )
        }


class TimeSlotAvailabilityForm(forms.ModelForm):
    class Meta:
        model = TimeSlotAvailability
        fields = ['specific_date', 'time_slot', 'is_available', 'is_booked']

    def __init__(self, *args, **kwargs):
        spa_service = kwargs.pop('spa_service', None)
        super().__init__(*args, **kwargs)

        if spa_service:
            time_slot_queryset = TimeSlot.objects.filter(
                spa_service=spa_service
            )
            self.fields['time_slot'].queryset = time_slot_queryset
        else:
            self.fields['time_slot'].queryset = TimeSlot.objects.none()


class FrontendTimeSlotForm(forms.ModelForm):
    time_slots = forms.ModelMultipleChoiceField(
        queryset=TimeSlot.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Available Time Slots"
    )

    class Meta:
        model = TimeSlotAvailability
        fields = ['specific_date', 'time_slots']

    def __init__(self, *args, **kwargs):
        self.availability = kwargs.pop('availability', None)
        super().__init__(*args, **kwargs)
        if self.availability:
            spa_service = self.availability.spa_service
            time_slots_queryset = TimeSlot.objects.filter(
                spa_service=spa_service
            )
            self.fields['time_slots'].queryset = time_slots_queryset
            self.initial['time_slots'] = TimeSlot.objects.filter(
                id__in=TimeSlotAvailability.objects.filter(
                    availability=self.availability,
                    specific_date=self.initial.get('specific_date')
                ).values_list('time_slot_id', flat=True)
            )
        else:
            self.fields['time_slots'].queryset = TimeSlot.objects.none()

    def save(self, commit=True):
        specific_date = self.cleaned_data['specific_date']
        selected_time_slots = self.cleaned_data['time_slots']

        if not self.availability:
            raise ValueError(
                "Availability must be set when saving "
                "TimeSlotAvailability instances."
            )

        try:
            with transaction.atomic():
                existing_time_slots = (
                    TimeSlotAvailability.objects.filter(
                        availability=self.availability,
                        specific_date=specific_date,
                    )
                )

                for tsa in existing_time_slots:
                    if tsa.is_booked:
                        continue
                    if tsa.time_slot in selected_time_slots:
                        tsa.is_available = True
                    else:
                        tsa.is_available = False
                    tsa.save()

                for time_slot in selected_time_slots:
                    TimeSlotAvailability.objects.update_or_create(
                        availability=self.availability,
                        specific_date=specific_date,
                        time_slot=time_slot,
                        defaults={'is_available': True, 'is_booked': False}
                    )

        except Exception as e:
            raise e

        return self.availability
