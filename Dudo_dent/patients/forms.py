from django import forms

from Dudo_dent.mixins import GetDentistsMixin
from Dudo_dent.patients.models import Patient


class PatientBaseForm(GetDentistsMixin, forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('full_name', 'date_of_birth', 'email', 'phone_number', 'personal_id', 'gender',)
        widgets = {
            'age': forms.NumberInput,
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






