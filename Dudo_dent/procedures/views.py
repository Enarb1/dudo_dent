from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from Dudo_dent.common.mixins.forms_mixins import SearchMixin
from Dudo_dent.common.mixins.redirect_mixins import ReturnToRedirectMixin
from Dudo_dent.common.mixins.views_mixins import EditDataMixin
from Dudo_dent.procedures.models import Procedure
from Dudo_dent.procedures.forms import ProcedureAddForm, ProcedureEditForm, SearchProcedureForm


# Create your views here.


class AllProcedures(SearchMixin, ListView):
    model = Procedure
    template_name = 'procedures/procedures-main.html'
    form_class = SearchProcedureForm
    search_param = 'name__icontains'
    
    def get_queryset(self):
        return super().get_queryset().order_by('name')

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


class EditProcedure(EditDataMixin, UpdateView):
    model = Procedure
    form_class = ProcedureEditForm
    template_name = 'procedures/edit-procedure.html'
    redirect_url = 'procedure-details'
    context_param = 'procedure'


class DeleteProcedure(DeleteView):
    model = Procedure
    success_url = reverse_lazy('all-procedures')
