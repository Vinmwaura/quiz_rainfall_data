from django.utils import timezone
from django.test import TestCase
from .models import Region, Rainfall
# Create your tests here.


class RegionMethodTests(TestCase):
    def setUp(self):
        self.region = Region.objects.create(
            region_name="Nairobi")

    def test_Region_object_creation(self):
        """
        Tests whether region object is created correctly
        and returns True if successful
        """
        self.assertTrue(isinstance(self.region, Region))

    def tearDown(self):
        self.region.delete()


class RainfallMethodTests(TestCase):
    def setUp(self):
        self.region = Region.objects.create(
            region_name="Nairobi")

        self.rainfall = Rainfall.objects.create(
            region=self.region,
            amount=100.1,
            date=timezone.now())

    def test_Rainfall_object_creation(self):
        """
        Tests whether rainfall object is created correctly
        and returns True if successful
        """
        self.assertTrue(isinstance(self.rainfall, Rainfall))

    def tearDown(self):
        self.rainfall.delete()
        self.region.delete()
