from django import forms
from .models import Review, SpaService, SpecificDate


class reviewForm(forms.ModelForm):
    """ Lets users review spa services. From Blog walkthroug"""
    class Meta:
        model = Review
        fields = ('body',)


class MultiDateInput(forms.TextInput):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'form-control', 'placeholder': 'Select multiple dates'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

class SpecificDateAdminForm(forms.ModelForm):
    dates = forms.CharField(
        widget=MultiDateInput(attrs={'id': 'specific_dates_picker'}),
        help_text='Enter multiple dates separated by commas (e.g., 2024-08-01, 2024-08-02)'
    )

    class Meta:
        model = SpecificDate
        fields = []

    def clean_dates(self):
        dates = self.cleaned_data.get('dates')
        if dates:
            date_list = [date.strip() for date in dates.split(',') if date.strip()]
            unique_dates = set(date_list)
            for date in unique_dates:
                if SpecificDate.objects.filter(date=date).exists():
                    raise forms.ValidationError(f"The date {date} already exists.")
            return unique_dates
        return []

    def save(self, commit=True):
        unique_dates = self.cleaned_data['dates']
        specific_date_objects = [SpecificDate(date=date) for date in unique_dates]
        SpecificDate.objects.bulk_create(specific_date_objects)
        return specific_date_objects
        

    class Media:
        js = ('https://cdn.jsdelivr.net/npm/flatpickr', 'admin/js/init_flatpickr.js')
        css = {
            'all': ('https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css',)
        }
