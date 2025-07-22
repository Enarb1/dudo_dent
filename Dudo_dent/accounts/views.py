from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.accounts.constants import PATIENT_PROFILE_FIELDS, WORK_PROFILE_FIELDS
from Dudo_dent.accounts.forms import PatientRegisterForm, CustomUserCreationBaseForm, RoleBasedUserCreationForm, \
    EditPatientProfileForm, EditWorkProfileForm
from Dudo_dent.accounts.services.profile_display import get_profile_fields
from Dudo_dent.common.mixins.permissions_mixins import OwnerAndRolePermissionMixin
from Dudo_dent.common.mixins.views_mixins import EditDataMixin
from Dudo_dent.visits.models import Visit

# Create your views here.
UserModel = get_user_model()


class UserRegisterView(CreateView):
    model = UserModel
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

    def get_form_class(self):

        if not self.request.user.is_authenticated:
            return PatientRegisterForm

        if self.request.user.is_staff:
            return CustomUserCreationBaseForm

        return RoleBasedUserCreationForm
    
    def get_form_kwargs(self):
        """We pass 'request_user' to the kwargs, to get the appropriate permissions for the user"""

        kwargs = super().get_form_kwargs()

        if self.get_form_class() == RoleBasedUserCreationForm:
            kwargs['request_user'] = self.request.user

        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)

        if not self.request.user.is_authenticated:
            login(self.request, self.object)

        return response




class UserProfileView(LoginRequiredMixin,OwnerAndRolePermissionMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details.html'
    allowed_roles = [UserTypeChoices.NURSE, UserTypeChoices.DENTIST]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        profile = user.get_profile()
        visits = Visit.objects.filter(patient__user=self.request.user)

        if profile:
            """Here we set what type of fields should be displayed"""
            field_map = PATIENT_PROFILE_FIELDS if user.is_patient else WORK_PROFILE_FIELDS

            context['profile_fields'] = get_profile_fields(field_map, profile, user)
        context['visits'] = visits

        return context

class EditProfileView(LoginRequiredMixin,OwnerAndRolePermissionMixin, EditDataMixin, UpdateView):
    model = UserModel
    template_name = 'accounts/edit-profile.html'
    redirect_url = 'profile'
    context_param = 'profile'

    allowed_roles = [UserTypeChoices.DENTIST]


    def get_form_class(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_patient:
                return EditPatientProfileForm

            return EditWorkProfileForm

    def get_initial(self):
        initial = super().get_initial()
        profile = self.request.user.get_profile()

        if profile.user.is_patient:
            initial.update({
                'personal_id':profile.personal_id,
                'gender':profile.gender,
            })
        else:
            initial.update({
                'address': profile.address,
            })

        initial.update({
            'phone_number': profile.phone_number,
            'date_of_birth': profile.date_of_birth,
        })

        return initial


class DeleteProfileView(LoginRequiredMixin,OwnerAndRolePermissionMixin, DeleteView):
    model = UserModel
    template_name = 'accounts/delete-profile.html'
    success_url = reverse_lazy('home')

    allowed_roles = [UserTypeChoices.DENTIST]

