from django.shortcuts import render

from Dudo_dent.visits.models import Visit


# Create your views here.


def all_visits(request):
    visits = Visit.objects.all().order_by('-date')

    context = {
        'visits': visits
    }

    return render(request, 'visits/visits-main.html', context)


def visit_by_id(request, pk):
    visit = Visit.objects.filter(pk=pk).first()

    context = {
        'visit': visit
    }
    return render(request, 'visits/visit-details.html', context)