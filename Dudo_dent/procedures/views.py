from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from Dudo_dent.common.mixins import ReturnToRedirectMixin
from Dudo_dent.procedures.models import Procedure
from Dudo_dent.procedures.forms import ProcedureAddForm, ProcedureEditForm, SearchProcedureForm


# Create your views here.


class AllProcedures(ListView):
    model = Procedure
    template_name = 'procedures/procedures-main.html'
    form_class = SearchProcedureForm
    query_param = 'query'
    
    def get_context_data(self, *, object_list = None, **kwargs):
        kwargs.update({
            'form': self.form_class(),
            'query': self.request.GET.get(self.query_param,''),
        })
        
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        queryset = self.model.objects.all()
        search_value = self.request.GET.get(self.query_param)

        if search_value:
            queryset = queryset.filter(
                name__icontains=search_value,
            )

        return queryset.order_by('name')

class ProcedureDetails(DetailView):
    model = Procedure
    template_name = 'procedures/procedure-details.html'


class AddProcedure(ReturnToRedirectMixin, CreateView):
    model = Procedure
    form_class = ProcedureAddForm
    template_name = 'procedures/add-procedure.html'
    return_to_param = 'return_to'
    redirect_targets = {
        'add-visit': reverse_lazy('add-visit'),
    }

    def get_default_success_url(self):
        return reverse_lazy('all-procedures')


class EditProcedure(UpdateView):
    model = Procedure
    form_class = ProcedureEditForm
    template_name = 'procedures/edit-procedure.html'

    def get_success_url(self):
        return reverse_lazy('procedure-details', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['procedure'] = self.object

        return context


class DeleteProcedure(DeleteView):
    model = Procedure
    success_url = reverse_lazy('all-procedures')
