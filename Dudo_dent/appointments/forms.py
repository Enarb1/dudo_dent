from django import forms
from django.contrib.auth import get_user_model

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.appointments.models import Appointment
from Dudo_dent.patients.models import Patient


UserModel = get_user_model()

class BaseAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ('created_at','end_time', 'google_event_id')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'additional_info': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Add Additional Info for your Appointment...',
                'style': 'resize: none',
            }),
        }


class AddAppointmentForm(BaseAppointmentForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


        self.fields['start_time'].label = 'Time'

        if user.is_patient:
            self.fields['patient'].initial = user
            self.fields['patient'].queryset = UserModel.objects.filter(id=user.id)
            self.fields['patient'].disabled = True
        else:
            self.fields['patient'].queryset = UserModel.objects.filter(role=UserTypeChoices.PATIENT)


class EditAppointmentForm(BaseAppointmentForm):
    pass


class DeleteAppointmentForm(BaseAppointmentForm):
    pass

