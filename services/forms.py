from django import forms
from .models import Review, SpaService, SpecificDate


class reviewForm(forms.ModelForm):
    """ Lets users review spa services. From Blog walkthroug"""
    class Meta:
        model = Review
        fields = ('body',)


from django import forms
from .models import SpecificDate

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

    def save(self, commit=True):
        dates = self.cleaned_data['dates']
        date_list = [date.strip() for date in dates.split(',') if date.strip()]
        specific_date_objects = []
        for date in date_list:
            specific_date = SpecificDate(date=date)
            specific_date_objects.append(specific_date)
        SpecificDate.objects.bulk_create(specific_date_objects)
        return specific_date_objects[0] if specific_date_objects else None


    class Media:
        js = ('https://cdn.jsdelivr.net/npm/flatpickr', 'admin/js/init_flatpickr.js')
        css = {
            'all': ('https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css',)
        }
