from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.accounts.constants import ALLOWED_ROLES_CREATION, USER_IS_STAFF
from Dudo_dent.patients.choices import PatientGenderChoices
import logging
logger = logging.getLogger(__name__)

UserModel = get_user_model()

class CustomUserCreationBaseForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('full_name', 'email', 'role')
        widgets = {}


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel
        fields = ('full_name', 'email')


class PatientRegisterForm(CustomUserCreationBaseForm):
    class Meta(CustomUserCreationBaseForm.Meta):
        exclude = ('role',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date_of_birth'] = forms.DateField(
            required=False,
            widget=forms.DateInput(attrs={'type': 'date'})
        )

        self.fields['personal_id'] = forms.CharField(
            required=False,
            max_length=30
        )

        self.fields['phone_number'] = forms.CharField(
            required=False
        )

        self.fields['gender'] = forms.ChoiceField(
            choices=PatientGenderChoices,
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = UserTypeChoices.PATIENT

        user.age = self.cleaned_data['date_of_birth']
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
        widget=forms.DateInput(attrs={'type': 'date'})
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

        user.phone_number = self.cleaned_data['phone_number']
        user.address = self.cleaned_data['address']
        user.date_of_birth = self.cleaned_data['date_of_birth']

        if commit:
            user.save()

        return user


class BaseProfileForm(forms.ModelForm):
    """Base form class for the Edit Profile Forms"""
    phone_number = forms.CharField(
        max_length=30,
        required=False,
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = UserModel
        fields = ('full_name', 'email',)


class EditPatientProfileForm(BaseProfileForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.fields['personal_id'] = forms.CharField(
            max_length=30,
            required=False,
        )

        self.fields['gender'] = forms.ChoiceField(
            choices=PatientGenderChoices,
        )

    
    def save(self, commit=True):
        """Save method for editing a patient's profile.

        We use commit=True here because the base form already handles saving fields
        on the CustomUser model ('full_name' and 'email').

        This method updates additional patient-specific fields stored in the related
        Patient profile, which is linked via a OneToOneField.

        If 'commit' is True, both the user and the patient profile are saved."""
        user = super().save(commit=commit)

        patient = user.get_profile()

        if patient:
            patient.gender = self.cleaned_data['gender']
            patient.date_of_birth = self.cleaned_data['date_of_birth']
            patient.phone_number = self.cleaned_data['phone_number']
            patient.personal_id = self.cleaned_data['personal_id']

            if commit:
                patient.save()

        return user


class EditWorkProfileForm(BaseProfileForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['address'] = forms.CharField(
            max_length=200,
            required=False
        )

    def save(self, commit=True):
        """Save method for editing a patient's profile.

        We use commit=True here because the base form already handles saving fields
        on the CustomUser model ('full_name' and 'email').

        This method updates additional workprofile-specific fields stored in the related
        WorkProfile profile, which is linked via a OneToOneField.

        If 'commit' is True, both the user and the patient profile are saved."""

        user = super().save(commit=commit)

        profile = user.get_profile()

        if profile:
            profile.phone_number = self.cleaned_data['phone_number']
            profile.date_of_birth = self.cleaned_data['date_of_birth']
            profile.address = self.cleaned_data['address']

            if commit:
                profile.save()

        return user
