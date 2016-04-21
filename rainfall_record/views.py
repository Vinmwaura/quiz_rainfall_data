from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RainfallForm, RecordForm
from .models import Region, Rainfall
from django.core.urlresolvers import reverse
from django.db.models import Sum
from matplotlib import pylab
from pylab import *
import PIL.Image

from django.http import HttpResponse
# Create your views here.


# View for homepage
def home(request):
    return render(request, 'rainfall_record/homepage.html', {})


# View for displayig graph, uses matplotlib to generate graph
# and pillow to display it using httpresponse
def display_graph(request, year):
    regions_object = Region.objects.all()  # region_objects
    amount_total = []  # List for storing sum ofamount in a region
    region_names = []  # List for storing region names
    for region in regions_object:
        region_names.append(region.region_name)
        # Filters Rainfall object by region and by year
        rainfall_data = Rainfall.objects.filter(
            date__year=year).filter(
            region=region)
        # If rainfall data is not empty, sum the amount
        if len(rainfall_data) > 0:
            amount_total.append(
                float(rainfall_data.aggregate(Sum('amount'))['amount__sum']))
        # Otherwise set to 0
        else:
            amount_total.append(0)

    # Generate bar graph using data obtained from
    # database using matplotlib
    y_pos = np.arange(len(region_names))
    plt.bar(y_pos, amount_total, align='center', alpha=0.5)
    plt.xticks(y_pos, region_names)
    plt.ylabel('Amount (mm)')
    plt.title('Regions')
    grid(True)

    # Converts bar graph into image using Pil
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.frombytes(
        "RGB",
        canvas.get_width_height(),
        canvas.tostring_rgb())

    pylab.close()
    response = HttpResponse(content_type="image/png")
    graphIMG.save(response, "PNG")

    # Returns image as HttpResponse
    return response


# View for display form to input rainfall data
def get_details(request):
    if request.method == 'POST':
        form = RainfallForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('rainfall:homepage'))
    else:
        form = RainfallForm()
    return render(
        request,
        'rainfall_record/rainfall_form.html',
        {'form': form})


# View containg form for selecting year to be
# used in displaying graph
def get_records(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            year_choices = form.cleaned_data['year_choices']
            return HttpResponseRedirect(
                reverse('rainfall:show_graph', args=(year_choices,)))
    else:
        form = RecordForm()
    return render(
        request,
        'rainfall_record/rainfall_chart.html',
        {'form': form})
