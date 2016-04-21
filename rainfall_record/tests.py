from django.utils import timezone
from django.test import TestCase
from .models import Region, Rainfall
from django.core.urlresolvers import reverse
import datetime
from rainfall_record.forms import RainfallForm, RecordForm
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


class HomepageViewTests(TestCase):
    def test_if_homepage_loads(self):
        """
        If view loads correctly, status code 200 will occur.
        """
        response = self.client.get(reverse('rainfall:homepage'))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "There are no categories present.")
        # self.assertQuerysetEqual(response.context['categories'], [])


class RainfallFormViewTests(TestCase):
    def test_if_rainfall_form_loads(self):
        """
        If view loads correctly, status code 200 will occur.
        """
        response = self.client.get(reverse('rainfall:records'))
        self.assertEqual(response.status_code, 200)

    def test_if_date_field_allows_future_date(self):
        """
        Tests whether date field allows future date to be posted
        """
        future_date = datetime.datetime.now() + datetime.timedelta(days=1)
        form_data = {
            'region': 'Nairobi',
            'amount': '100.0',
            'date': future_date}
        form = RainfallForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_if_amount_field_allows_negative_values(self):
        """
        Tests whether amount field allows negative amounts to be posted
        """
        current_date = datetime.datetime.now()
        form_data = {
            'region': 'Nairobi',
            'amount': '-100.0',
            'date': current_date}
        form = RainfallForm(data=form_data)
        self.assertFalse(form.is_valid())


class RainfallChartViewTests(TestCase):
    def test_if_rainfall_chart_loads(self):
        """
        If view loads correctly, status code 200 will occur.
        """
        response = self.client.get(reverse('rainfall:graph'))
        self.assertEqual(response.status_code, 200)
