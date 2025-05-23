from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from Dudo_dent.patients.forms import SearchPatientForm
from Dudo_dent.visits.forms import VisitBaseForm, VisitCreateForm, VisitEditForm
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

    if 'visit_form_data' in request.session:
        form = VisitCreateForm(request.session.pop('visit_form_data'))
    else:
        form= VisitCreateForm(request.POST or None)

    if request.method == 'POST':

        if 'add-patient' in request.POST:
            request.session['visit_form_data'] = request.POST
            return redirect(reverse('add-patient') + '?return_to=add-visit')

        if 'add-procedure' in request.POST:
            request.session['visit_form_data'] = request.POST
            return redirect(reverse('add-procedure') + '?return_to=add-visit')

        if form.is_valid():
            form.save()
            return redirect('all-visits')

    context = {
        'form': form
    }

    return render(request, 'visits/add-visit.html', context)


def edit_visit(request, pk):
    visit = get_object_or_404(Visit, pk=pk)

    if request.method == 'POST':
        form = VisitEditForm(request.POST, instance=visit)

        if form.is_valid():
            form.save()
            return redirect('visit-details', pk=visit.pk)

    else:
        form = VisitEditForm(instance=visit)

    context = {
        'form': form,
        'visit': visit
    }

    return render(request,'visits/edit-visit.html', context)



def delete_visit(request, pk):
    visit = get_object_or_404(Visit, pk=pk)
    if request.method == 'POST':
        visit.delete()
        return redirect('all-visits',)

    return redirect('visit-details', pk=visit.pk)
