from django.shortcuts import render, redirect

from Dudo_dent.patients.forms import SearchPatientForm
from Dudo_dent.visits.forms import VisitBaseForm
from Dudo_dent.visits.models import Visit


# Create your views here.


def all_visits(request):
    visits = Visit.objects.all().order_by('-date')
    form = SearchPatientForm(request.GET)

    if request.method == 'GET':
        if form.is_valid():
            query = form.cleaned_data['query']
            visits = visits.filter(patient__full_name__icontains=query).order_by('-date')

    context = {
        'visits': visits,
        'form': form
    }

    return render(request, 'visits/visits-main.html', context)


def visit_by_id(request, pk):
    visit = Visit.objects.filter(pk=pk).first()

    context = {
        'visit': visit
    }
    return render(request, 'visits/visit-details.html', context)


def add_visit(request):
    form= VisitBaseForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('all-visits')
    else:
        print(form.errors)


    context = {
        'form': form
    }

    return render(request, 'visits/add-visit.html', context)

