from django import forms

from Dudo_dent.patients.models import Patient


class PatientBaseForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('full_name', 'age', 'email', 'phone_number', 'personal_id', 'gender')
        widgets = {
            'age': forms.NumberInput,
            'email': forms.EmailInput,
        }


class PatientCreateForm(PatientBaseForm):
    pass


class PatientEditForm(PatientBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PatientDeleteForm(PatientBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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






