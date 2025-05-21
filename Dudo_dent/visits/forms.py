from django import forms

from Dudo_dent.visits.models import Visit


class VisitBaseForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'additional_info': forms.Textarea()
        }


class VisitCreateForm(VisitBaseForm):
    pass


class VisitEditForm(VisitBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VisitDeleteForm(VisitBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)