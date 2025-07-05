from email.policy import default

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.accounts.constants import ALLOWED_ROLES_CREATION, USER_IS_STAFF
from Dudo_dent.patients.choices import PatientGenderChoices

UserModel = get_user_model()

class CustomUserCreationBaseForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('full_name', 'email', 'role')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel
        fields = ('full_name', 'email')


class PatientRegisterForm(CustomUserCreationBaseForm):
    class Meta(CustomUserCreationBaseForm.Meta):
        exclude = ('role',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['age'] = forms.IntegerField(
            required=False,
        )

        self.fields['personal_id'] = forms.CharField(
            max_length=30
        )

        self.fields['phone_number'] = forms.CharField(
            required=False
        )

        self.fields['gender'] = forms.ChoiceField(
            choices=PatientGenderChoices,
            required=False,
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = UserTypeChoices.PATIENT

        user.age = self.cleaned_data['age']
        user.personal_id = self.cleaned_data['personal_id']
        user.phone_number = self.cleaned_data['phone_number']
        user.gender = self.cleaned_data['gender']

        if commit:
            user.save()

        return user


class RoleBasedUserCreationForm(CustomUserCreationBaseForm):
    phone_number = forms.CharField(
        max_length=30,
        required=False
    )
    address =  forms.CharField(
        max_length=200,
        required=False
    )
    date_of_birth = forms.DateField(
        required=False,
    )

    def __init__(self, *args, **kwargs):
        """Extracting the logged-in user, so that we get the profile creation permission for him later"""
        self.request_user = kwargs.pop('request_user', None)

        super().__init__(*args, **kwargs)

        """Getting the allowed profile creation choices for the logged-in user, 
        with values for safety, so that the program does not crash"""
        self.allowed_roles = ALLOWED_ROLES_CREATION.get(
            getattr(self.request_user, 'role', ''),[]
        )
        self.fields['role'].choices = [(r.value, r.label) for r in self.allowed_roles]

    def clean_role(self):
        role = self.cleaned_data['role']

        """We make this validation to make sure there were no manipulations done from the frontend"""
        if role not in [r.value for r in self.allowed_roles]:
            raise forms.ValidationError("You are not allowed create a user with that role.")
        return role

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.is_staff = USER_IS_STAFF.get(user.role, False)

        if commit:
            user.save()

        return user




