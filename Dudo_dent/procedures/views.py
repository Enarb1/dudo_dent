from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.common.mixins.forms_mixins import SearchMixin
from Dudo_dent.common.mixins.permissions_mixins import RoleRequiredMixin
from Dudo_dent.common.mixins.redirect_mixins import ReturnToRedirectMixin
from Dudo_dent.common.mixins.views_mixins import EditDataMixin, DeleteCancelMixIn
from Dudo_dent.procedures.models import Procedure
from Dudo_dent.procedures.forms import ProcedureAddForm, ProcedureEditForm, SearchProcedureForm

import logging
logger = logging.getLogger(__name__)

# Create your views here.


class AllProcedures(LoginRequiredMixin,RoleRequiredMixin, SearchMixin, ListView):
    model = Procedure
    template_name = 'procedures/procedures-main.html'
    form_class = SearchProcedureForm
    search_param = 'name__icontains'

    paginate_by = 21

    allowed_roles = [UserTypeChoices.NURSE, UserTypeChoices.DENTIST]
    
    def get_queryset(self):
        return super().get_queryset().order_by('name')

class ProcedureDetails(LoginRequiredMixin,RoleRequiredMixin,DetailView):
    model = Procedure
    template_name = 'procedures/procedure-details.html'

    allowed_roles = [UserTypeChoices.NURSE, UserTypeChoices.DENTIST]


class AddProcedure(LoginRequiredMixin,RoleRequiredMixin,ReturnToRedirectMixin, CreateView):
    model = Procedure
    form_class = ProcedureAddForm
    template_name = 'procedures/add-procedure.html'
    return_to_param = 'return_to'
    redirect_targets = {
        'add-visit': reverse_lazy('add-visit'),
    }

    allowed_roles = [UserTypeChoices.NURSE, UserTypeChoices.DENTIST]

    def get_default_success_url(self):
        return reverse_lazy('all-procedures')


class EditProcedure(LoginRequiredMixin,RoleRequiredMixin,EditDataMixin, UpdateView):
    model = Procedure
    form_class = ProcedureEditForm
    template_name = 'procedures/edit-procedure.html'
    redirect_url = 'procedure-details'
    context_param = 'procedure'

    allowed_roles = [UserTypeChoices.NURSE, UserTypeChoices.DENTIST]


class DeleteProcedure(LoginRequiredMixin, RoleRequiredMixin, DeleteCancelMixIn, DeleteView):
    model = Procedure
    template_name = 'delete-conformation.html'
    success_url = reverse_lazy('all-procedures')
    cancel_url = 'procedure-details'

    allowed_roles = [UserTypeChoices.DENTIST]
