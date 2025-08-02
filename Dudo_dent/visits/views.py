from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.common.mixins.forms_mixins import SearchMixin
from Dudo_dent.common.mixins.permissions_mixins import RoleRequiredMixin, OwnerAndRolePermissionMixin
from Dudo_dent.common.mixins.redirect_mixins import MultiStepRedirectMixin, ReturnToRedirectMixin
from Dudo_dent.common.mixins.views_mixins import EditDataMixin
from Dudo_dent.patients.forms import SearchPatientForm
from Dudo_dent.visits.forms import VisitCreateForm, VisitEditForm
from Dudo_dent.visits.models import Visit

import logging
logger = logging.getLogger(__name__)

# Create your views here.


class AllVisits(LoginRequiredMixin,RoleRequiredMixin,SearchMixin, ListView):
    model = Visit
    template_name = 'visits/visits-main.html'
    form_class = SearchPatientForm
    search_param = 'patient__full_name__icontains'
    paginate_by = 5

    allowed_roles = [UserTypeChoices.NURSE, UserTypeChoices.DENTIST]

    def get_queryset(self):
        return super().get_queryset().order_by('-date')


class VisitDetails(LoginRequiredMixin,OwnerAndRolePermissionMixin, DetailView):
    model = Visit
    template_name = 'visits/visit-details.html'

    allowed_roles = [UserTypeChoices.NURSE, UserTypeChoices.DENTIST]

    def test_func(self):
        visit = self.get_object()
        user_to_view = visit.patient.user
        current_user = self.request.user

        return (
                current_user.is_authenticated and
                (current_user == user_to_view or
                 self.has_required_role(current_user)
                 ))


class VisitCreate(LoginRequiredMixin,RoleRequiredMixin,MultiStepRedirectMixin, ReturnToRedirectMixin, CreateView):
    model = Visit
    template_name = 'visits/add-visit.html'
    form_class = VisitCreateForm

    session_key = 'visit_form_data'
    return_to_param = 'return_to'
    return_to_value = 'add-visit'
    redirect_actions = {
        'add-patient': 'add-patient',
        'add-procedure': 'add-procedure',
    }
    redirect_targets = {
        'add-patient': reverse_lazy('add-patient'),
        'add-procedure': reverse_lazy('add-procedure'),
    }

    allowed_roles = [UserTypeChoices.NURSE, UserTypeChoices.DENTIST]

    def get_default_success_url(self):
        return reverse_lazy('all-visits')


class VisitUpdate(LoginRequiredMixin,RoleRequiredMixin,EditDataMixin, UpdateView):
    model = Visit
    template_name = 'visits/edit-visit.html'
    form_class = VisitEditForm
    redirect_url = 'visit-details'
    context_param = 'visit'\

    allowed_roles = [UserTypeChoices.NURSE, UserTypeChoices.DENTIST]


class DeleteVisit(LoginRequiredMixin,RoleRequiredMixin,DeleteView):
    model = Visit
    success_url = reverse_lazy('all-visits')

    allowed_roles = [UserTypeChoices.DENTIST]
