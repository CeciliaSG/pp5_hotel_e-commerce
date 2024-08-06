from django import forms
from .models import Review, SpaService


class reviewForm(forms.ModelForm):
    """ Lets users review spa services. From Blog walkthroug"""
    class Meta:
        model = Review
        fields = ('body',)