from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.accounts.constants import PATIENT_PROFILE_FIELDS
from Dudo_dent.accounts.services.profile_display import get_profile_fields
from Dudo_dent.common.mixins.forms_mixins import SearchMixin
from Dudo_dent.common.mixins.permissions_mixins import RoleRequiredMixin
from Dudo_dent.common.mixins.redirect_mixins import ReturnToRedirectMixin
from Dudo_dent.common.mixins.views_mixins import EditDataMixin, DeleteCancelMixIn
from Dudo_dent.patients.forms import PatientCreateForm, PatientEditForm, SearchPatientForm
from Dudo_dent.patients.models import Patient


# Create your views here.

class AllPatientsView(LoginRequiredMixin, RoleRequiredMixin, SearchMixin, ListView):
    model = Patient
    template_name = 'patients/patients-main.html'
    form_class = SearchPatientForm
    search_param = 'full_name__icontains'
    paginate_by = 21

    allowed_roles = [UserTypeChoices.NURSE, UserTypeChoices.DENTIST]


class PatientDetailsView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/patient-details.html'

    allowed_roles = [UserTypeChoices.NURSE, UserTypeChoices.DENTIST]

    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        patient = self.get_object()
        visits = self.object.visits.all().order_by('-date')
        context['visit_list'] = visits
        context['profile_fields'] = get_profile_fields(PATIENT_PROFILE_FIELDS, profile=patient, user=None)

        return context


class PatientCreateView(LoginRequiredMixin, RoleRequiredMixin, ReturnToRedirectMixin, CreateView):
    model = Patient
    form_class = PatientCreateForm
    template_name = 'patients/add-patient.html'
    return_to_param = 'return_to'
    redirect_targets = {
        'add-visit': reverse_lazy('add-visit'),
    }

    allowed_roles = [UserTypeChoices.NURSE, UserTypeChoices.DENTIST]

    def get_default_success_url(self):
        return reverse_lazy('all-patients')


class EditPatientView(LoginRequiredMixin, RoleRequiredMixin, EditDataMixin, UpdateView):
    model = Patient
    form_class = PatientEditForm
    template_name = 'patients/edit-patient.html'

    redirect_url = 'patient-details'
    context_param = 'patient'
    get_object_by = 'pk'

    allowed_roles = [UserTypeChoices.NURSE, UserTypeChoices.DENTIST]


class DeletePatientView(LoginRequiredMixin, RoleRequiredMixin,DeleteCancelMixIn, DeleteView):
    # with conformation form
    model = Patient
    template_name = 'delete-conformation.html'
    success_url = reverse_lazy('all-patients')
    cancel_url = 'patient-details'

    allowed_roles = [UserTypeChoices.DENTIST]
