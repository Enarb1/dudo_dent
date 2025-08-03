from django import forms
from django.contrib.auth import get_user_model

from Dudo_dent.appointments.choices import WeekdayChoices
from Dudo_dent.appointments.models import Appointment, AvailabilityRule, UnavailabilityRule
from Dudo_dent.patients.models import Patient
import logging
logger = logging.getLogger(__name__)

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

class AddAppointmentChooseDentistForm(BaseAppointmentForm):
    """
    In the __init__ method we define what to be shown, based on the User Type
    """
    class Meta(BaseAppointmentForm.Meta):
        fields = ['patient', 'dentist']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user.is_patient:
            patient_instance = getattr(user, 'patient', None)
            self.fields['patient'].initial = patient_instance
            self.fields['patient'].queryset = Patient.objects.filter(user=user)
            self.fields['patient'].disabled = True
        else:
            self.fields['patient'].queryset = Patient.objects.all()

class AddAppointmentChooseDateForm(BaseAppointmentForm):
    """
    In the __init__ method we get the available dates from the view and
    pass them into the Select field in '%B %d, %Y' format.
    """
    class Meta(BaseAppointmentForm.Meta):
        fields = ['date']

    def __init__(self, *args, **kwargs):
        available_dates = kwargs.pop('available_dates', [])
        super().__init__(*args, **kwargs)

        self.fields['date'].widget = forms.Select(
            choices=[(d, d.strftime('%B %d, %Y')) for d in available_dates]
        )


class AddAppointmentChooseTimeForm(BaseAppointmentForm):
    """
    In the __init__ method we get the available time slots  from the view and
    pass them into the Select field in '%H:%M' format.
    """


    class Meta(BaseAppointmentForm.Meta):
        fields = ['start_time', 'additional_info']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'additional_info': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Add Additional Info for your Appointment...',
                'style': 'resize: none',
            }),
        }

    def __init__(self, *args, **kwargs):
        available_times = kwargs.pop('available_times', [])
        super().__init__(*args, **kwargs)

        self.fields['start_time'].label = 'Time'
        self.fields['start_time'].widget = forms.Select(
            choices=[(t.strftime('%H:%M'), t.strftime('%H:%M')) for t in available_times]
        )


class EditAppointmentForm(BaseAppointmentForm):
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        dentist = cleaned_data.get('dentist')

        if date and start_time and dentist:
            appointment = Appointment.objects.filter(
                date=date,
                start_time=start_time,
                dentist=dentist
            ).exclude(pk=self.instance.pk).exists()

            if appointment:
                raise forms.ValidationError("There is an appointment for this date and time!")

        return cleaned_data


class DeleteAppointmentForm(BaseAppointmentForm):
    pass


class SetAvailabilityForm(forms.ModelForm):
    weekdays = forms.MultipleChoiceField(
        choices=WeekdayChoices,
        widget=forms.SelectMultiple(attrs={
            'class': 'w-full border px-2 py-1 rounded',
            'size': 4
        }),
    )

    class Meta:
        model = AvailabilityRule
        exclude = ('dentist',)
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'valid_from': forms.DateInput(attrs={'type': 'date'}),
            'valid_to': forms.DateInput(attrs={'type': 'date'}),
        }


class DeleteAvailabilityForm(SetAvailabilityForm):
    pass


class SetUnavailableForm(forms.ModelForm):
    class Meta:
        model = UnavailabilityRule
        exclude = ('dentist',)
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea()
        }

class DeleteUnavailableForm(SetUnavailableForm):
    pass