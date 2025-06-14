from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, CreateView

from Dudo_dent.common.mixins import MainViewsMixin, ReturnToRedirectMixin, MultiStepRedirectMixin
from Dudo_dent.patients.forms import SearchPatientForm
from Dudo_dent.visits.forms import VisitBaseForm, VisitCreateForm, VisitEditForm
from Dudo_dent.visits.models import Visit


# Create your views here.


class AllVisits(MainViewsMixin, ListView):
    model = Visit
    template_name = 'visits/visits-main.html'
    form_class = SearchPatientForm
    search_param = 'patient__full_name__icontains'

    def get_queryset(self):
        return super().get_queryset().order_by('-date')


class VisitDetails(DetailView):
    model = Visit
    template_name = 'visits/visit-details.html'


class VisitCreate(MultiStepRedirectMixin, ReturnToRedirectMixin, CreateView):
    model = Visit
    template_name = 'visits/add-visit.html'
    form_class = VisitCreateForm

    session_key = 'visit_form_data'
    return_to_param = 'redirect_to'
    return_to_value = 'add-visit'
    redirect_actions = {
        'add-patient': 'add-patient',
        'add-procedure': 'add-procedure',
    }
    redirect_targets = {
        'add-patient': reverse('add-patient'),
        'add-procedure': reverse('add-procedure'),
    }

    def get_default_success_url(self):
        return reverse_lazy('all-visits')



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
