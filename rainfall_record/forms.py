from .models import Rainfall, Region
from django import forms
from django.core.validators import MinValueValidator
import datetime


class RainfallForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RainfallForm, self).__init__(*args, **kwargs)
        region = forms.ChoiceField(
            choices=Region.objects.all(),
            widget=forms.Select,
            required=True)

    amount = forms.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(0.0)],
        required=True)
    date = forms.DateField(
        widget=forms.SelectDateWidget())

    class Meta:
        model = Rainfall
        fields = ['region', 'amount', 'date']


class RecordForm(forms.Form):
    min_year = 1990
    current_year = datetime.date.today().year
    if min_year < current_year:
        years = [(x, x) for x in range(min_year, current_year + 1)]
    else:
        years = []

    year_choices = forms.ChoiceField(
        choices=years,
        widget=forms.Select,
        required=True)
