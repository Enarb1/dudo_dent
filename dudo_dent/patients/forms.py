from django import forms
from django.utils.translation import gettext_lazy as _

from dudo_dent.patients.models import Patient

import logging
logger = logging.getLogger(__name__)

class PatientBaseForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('full_name', 'date_of_birth', 'email', 'phone_number', 'personal_id', 'gender',)
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Име и Фамилия'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Въведете валиден имейл адрес'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Телефон (полето не е задължително)'}),
            'personal_id': forms.TextInput(attrs={'placeholder': 'ЕГН (полето не е задължително)'}),
        }
        labels = {
            'full_name': _('Име'),
            'date_of_birth': _('Дата на раждане'),
            'phone_number': _('Телефон'),
            'personal_id': _('ЕГН'),
            'gender': _('Пол'),
        }

class PatientCreateForm(PatientBaseForm):
    pass


class PatientEditForm(PatientBaseForm):
    pass

class PatientDeleteForm(PatientBaseForm):
    pass


class SearchPatientForm(forms.Form):

    query = forms.CharField(
        label='',
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Намери пациент...',
                'class': 'search-input',
            }
        )
    )






