from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from Dudo_dent.common.mixins import MainViewsMixin, ReturnToRedirectMixin, MultiStepRedirectMixin, EditDataMixin
from Dudo_dent.patients.forms import SearchPatientForm
from Dudo_dent.visits.forms import VisitCreateForm, VisitEditForm
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
        'add-patient': reverse_lazy('add-patient'),
        'add-procedure': reverse_lazy('add-procedure'),
    }

    def get_default_success_url(self):
        return reverse_lazy('all-visits')


class VisitUpdate(EditDataMixin, UpdateView):
    model = Visit
    template_name = 'visits/edit-visit.html'
    form_class = VisitEditForm
    redirect_url = 'visit-details'
    context_param = 'visit'


class DeleteVisit(DeleteView):
    model = Visit
    success_url = reverse_lazy('all-visits')
