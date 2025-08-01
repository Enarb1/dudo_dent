from django.contrib.auth import get_user_model
from django.test import TestCase

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.accounts.forms import PatientRegisterForm, RoleBasedUserCreationForm
from Dudo_dent.patients.choices import PatientGenderChoices


UserModel = get_user_model()

class TestRegistrationForm(TestCase):

    def setUp(self):
        self.patient_data = {
            "full_name": "Test User",
            "email": "test@test.com",
            "password1": "12branko34",
            "password2": "12branko34",
            "role": UserTypeChoices.PATIENT,
            "gender": PatientGenderChoices.MALE,
        }

        self.work_profile_data = {
            "full_name": "Test User",
            "email": "test@test.com",
            "password1": "12branko34",
            "password2": "12branko34",

        }

    def test_registration_patient_form_expect_success(self):
        form = PatientRegisterForm(data=self.patient_data)
        self.assertTrue(form.is_valid())

    def test_is_form_save_method_if_passing_patient_type_profile_for_patient(self):
        form = PatientRegisterForm(data=self.patient_data)
        self.assertEqual(form.data["role"], UserTypeChoices.PATIENT)

    def test_is_form_save_method_if_passing_dentist_type_profile_for_patient(self):
        self.work_profile_data['role'] = UserTypeChoices.DENTIST
        form = RoleBasedUserCreationForm(data=self.work_profile_data)
        self.assertEqual(form.data["role"], UserTypeChoices.DENTIST)

    def test_is_form_save_method_if_passing_nurse_type_profile_for_patient(self):
        self.work_profile_data['role'] = UserTypeChoices.NURSE
        form = RoleBasedUserCreationForm(data=self.work_profile_data)
        self.assertEqual(form.data["role"], UserTypeChoices.NURSE)

    def test_registration_from_missmatch_passwort(self):
        self.patient_data['password2'] = '12admin34'
        form = PatientRegisterForm(data=self.patient_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'password2': ['The two password fields didn’t match.']})

    def test_nurse_creating_dentist_profile_expect_error_message(self):
        nurse_user = UserModel.objects.create_user(
            full_name="Nurse User",
            email="n@nurse.com",
            password="12branko34",
            role=UserTypeChoices.NURSE,
        )

        self.work_profile_data['role'] = UserTypeChoices.DENTIST
        form = RoleBasedUserCreationForm(data=self.work_profile_data, request_user=nurse_user)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['role'],
            ['Select a valid choice. dentist is not one of the available choices.'])




