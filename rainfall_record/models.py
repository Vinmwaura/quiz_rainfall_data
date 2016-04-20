from django.db import models

# Create your models here.


class Region(models.Model):
    region_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.region_name


class Rainfall(models.Model):
    region = models.ForeignKey(Region)
    amount = models.DecimalField(max_digits=5, decimal_places=1, default=0.00)
    date = models.DateTimeField()

    def __str__(self):
        return "Region: ", self.region, " Date: ", self.date, " Amount: ", self.amount
