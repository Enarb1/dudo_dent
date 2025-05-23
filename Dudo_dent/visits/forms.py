from django import forms

from Dudo_dent.procedures.models import Procedure
from Dudo_dent.visits.models import Visit


class VisitBaseForm(forms.ModelForm):
    procedure = forms.ModelMultipleChoiceField(
        queryset=Procedure.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': 6,
        }),
    )

    class Meta:
        model = Visit
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'additional_info': forms.Textarea(attrs={'rows': 4}),
        }


class VisitCreateForm(VisitBaseForm):
    pass


class VisitEditForm(VisitBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VisitDeleteForm(VisitBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)