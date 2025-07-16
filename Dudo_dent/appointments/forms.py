from django import forms

from Dudo_dent.appointments.models import Appointment


class BaseAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ('created_at','end_time', 'google_event_id')


class AddAppointmentForm(BaseAppointmentForm):
    pass