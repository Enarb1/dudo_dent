from django.urls import reverse_lazy
from django.views.generic import CreateView

from Dudo_dent.accounts.forms import CustomUserCreationForm
from Dudo_dent.accounts.models import CustomUser, Profile
from Dudo_dent.patients.models import Patient


# Create your views here.


class PatientRegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        cleaned_data = form.cleaned_data

        try:
            patient = Patient.objects.get(personal_id=cleaned_data['personal_id'])
        except Patient.DoesNotExist:
            patient = Patient.objects.create(
                full_name=cleaned_data['full_name'],
                age=cleaned_data['age'],
                gender=cleaned_data['gender'],
                email=user.email,
                personal_id=cleaned_data['personal_id'],
                phone_number=cleaned_data['phone_number'],
                dentist=CustomUser.objects.get(id=cleaned_data['dentist']),
            )

        Profile.objects.create(
            user=user,
            full_name=cleaned_data['full_name'],
            age=cleaned_data['age'],
            gender=cleaned_data['gender'],
            phone_number=cleaned_data['phone_number'],
            patient=patient,
        )

        return response