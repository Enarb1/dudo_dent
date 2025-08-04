from django import forms

from dudo_dent.patients.models import Patient

import logging
logger = logging.getLogger(__name__)

class PatientBaseForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('full_name', 'date_of_birth', 'email', 'phone_number', 'personal_id', 'gender',)
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput,
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
                'placeholder': 'Search for patients...',
                'class': 'search-input',
            }
        )
    )






