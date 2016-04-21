from .models import Rainfall, Region
from django import forms
from django.core.validators import MinValueValidator
import datetime


class RainfallForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Class inheritance is to allow choices of region field to
        # be obtained from queryset of Region model
        super(RainfallForm, self).__init__(*args, **kwargs)
        # region field that uses data from Region model
        region = forms.ChoiceField(
            choices=Region.objects.all(),
            widget=forms.Select,
            required=True)

    # Amount field that gets decimal values of rainfall
    # can't benegative value
    amount = forms.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(0.0)],
        required=True)

    # Date the record was taken, can't be greater than the current date
    date = forms.DateField(
        widget=forms.SelectDateWidget())

    class Meta:
        model = Rainfall
        fields = ['region', 'amount', 'date']


class RecordForm(forms.Form):
    min_year = 2000  # Sets the lowest year that can be selected
    current_year = datetime.date.today().year  # Gets the current year
    # Validates if current year selected is greater than minimun set
    if min_year < current_year:
        # Sets the choices starting with the current year
        # and decreases to the minimum
        years = [(x, x) for x in range(current_year, min_year, -1)]
    else:
        years = []

    year_choices = forms.ChoiceField(
        choices=years,
        widget=forms.Select,
        required=True)
