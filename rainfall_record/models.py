from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MinValueValidator
# Create your models here.
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import date


def validate_date(value):
    date_today = date.today()
    if value > date_today:
        raise ValidationError(
            _('%(value)s is invalid. You can not set date in the future.'),
            params={'value': value},
        )


@python_2_unicode_compatible
class Region(models.Model):
    region_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return str(self.region_name)


@python_2_unicode_compatible
class Rainfall(models.Model):
    region = models.ForeignKey(Region)
    amount = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0.0,
        validators=[MinValueValidator(0.0)])
    date = models.DateField(validators=[validate_date])

    def __str__(self):
        return str(self.region) + "-" + str(self.date)
