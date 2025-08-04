from django import forms

from dudo_dent.procedures.models import Procedure
from dudo_dent.visits.models import Visit

import logging
logger = logging.getLogger(__name__)

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
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].label = ''


class VisitCreateForm(VisitBaseForm):
    pass


class VisitEditForm(VisitBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VisitDeleteForm(VisitBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)