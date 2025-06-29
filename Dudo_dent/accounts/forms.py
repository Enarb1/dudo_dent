from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from collections import OrderedDict

from Dudo_dent.accounts.models import CustomUser
from Dudo_dent.patients.choices import PatientGenderChoices


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Full Name....'}),
    )


    personal_id = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Personal ID (EGN)....'}),
    )

    phone_number = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number....'}),
    )

    gender = forms.ChoiceField(
        choices=PatientGenderChoices
    )

    age = forms.IntegerField()

    dentist = forms.ChoiceField(choices=[])

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        dentists = [d for d in CustomUser.objects.all() if d.is_dentist]
        self.fields['dentist'].choices = [(d.id, d.username) for d in dentists]

        field_order = [
            'full_name',
            'username',
            'personal_id',
            'email',
            'password1',
            'password2',
            'phone_number',
            'gender',
            'age',
            'dentist',
        ]

        self.fields = OrderedDict((key, self.fields[key]) for key in field_order if key in self.fields)


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = '__all__'