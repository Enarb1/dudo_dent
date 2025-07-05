from django.contrib.auth import get_user_model, login
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from Dudo_dent.accounts.constants import PATIENT_PROFILE_FIELDS, WORK_PROFILE_FIELDS
from Dudo_dent.accounts.forms import PatientRegisterForm, CustomUserCreationBaseForm, RoleBasedUserCreationForm
from Dudo_dent.accounts.services.profile_display import get_profile_fields

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
        kwargs['request_user'] = self.request.user

        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)

        if not self.request.user.is_authenticated:
            login(self.request, self.object)

        return response


class UserProfileView(DetailView):
    model = UserModel
    template_name = 'accounts/profile-details.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        profile = user.get_profile()

        if profile:
            """Here we set what type of fields should be displayed"""
            field_map = PATIENT_PROFILE_FIELDS if user.is_patient() else WORK_PROFILE_FIELDS

            context['profile_fields'] = get_profile_fields(field_map, profile, user)

        return context

















