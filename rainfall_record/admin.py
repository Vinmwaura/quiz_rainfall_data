from django.contrib import admin
from .models import Region, Rainfall
# Register your models here.


class RainfallAdmin(admin.ModelAdmin):
    model = Rainfall
    list_filter = ['date', 'region']
    search_fields = ['date']

admin.site.register(Region)
admin.site.register(Rainfall, RainfallAdmin)
