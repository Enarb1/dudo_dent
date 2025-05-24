from django import forms

from Dudo_dent.procedures.models import Procedure

class ProcedureBaseForm(forms.ModelForm):
    class Meta:
        model = Procedure
        fields = '__all__'


class ProcedureAddForm(ProcedureBaseForm):
    pass


class ProcedureEditForm(ProcedureBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProcedureDeleteForm(ProcedureBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SearchProcedureForm(forms.Form):
    query = forms.CharField(
        label='',
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search for procedure...',
                'class': 'search-input',
            }
        )
    )