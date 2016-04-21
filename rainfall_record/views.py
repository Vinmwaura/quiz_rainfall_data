from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RainfallForm, RecordForm
from .models import Region, Rainfall
from django.core.urlresolvers import reverse
from django.db.models import Sum
from matplotlib import pylab
from pylab import *
import PIL
import PIL.Image

from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(request, 'rainfall_record/homepage.html', {})


def display_graph(request, year):
    print(year)
    regions_object = Region.objects.all()
    amount_total = []
    region_names = []

    for region in regions_object:
        region_names.append(region.region_name)
        rainfall_data = Rainfall.objects.filter(
            date__year=year).filter(
            region=region)

        if len(rainfall_data) > 0:
            amount_total.append(
                float(rainfall_data.aggregate(Sum('amount'))['amount__sum']))

        else:
            amount_total.append(0)

    y_pos = np.arange(len(region_names))

    plt.bar(y_pos, amount_total, align='center', alpha=0.5)
    plt.xticks(y_pos, region_names)
    plt.ylabel('Amount (mm)')
    plt.title('Regions')
    grid(True)

    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.frombytes(
        "RGB",
        canvas.get_width_height(),
        canvas.tostring_rgb())
    # graphIMG.save(buffer, "PNG")
    pylab.close()
    response = HttpResponse(content_type="image/png")
    graphIMG.save(response, "PNG")
    return response
    # return HttpResponse(buffer.getvalue())


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
