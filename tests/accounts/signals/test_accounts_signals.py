from unittest.mock import patch, MagicMock

from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.test import TestCase

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.accounts.models import WorkProfile, CustomUser
from Dudo_dent.accounts.services.user_profile_services import handle_patient_profile, handle_work_profile
from Dudo_dent.accounts.signals import create_profile, create_google_calendar_for_dentist
from Dudo_dent.patients.choices import PatientGenderChoices
from Dudo_dent.patients.models import Patient



class TestSignalsProfileCreation(TestCase):

    def setUp(self):
        """
        Disconnecting signal to prevent auto-execution during save.
        Ensuring to reconnect the signal even on failure.
        Setting up the patient user.
        We ensure that 'Dentist' group exists, because handle_work_profile() will try to add the user to the Group.
        """
        post_save.disconnect(create_profile, sender=CustomUser)
        self.addCleanup(post_save.connect, create_profile, sender=CustomUser)

        Group.objects.create(name="Dentist")


    def _create_patient_user(self):
        user = CustomUser.objects.create_user(
            full_name="Patient One",
            email="p@test.com",
            role=UserTypeChoices.PATIENT,
            password='12branko34'
        )

        user.gender = PatientGenderChoices.OTHER
        user.save()

        return user

    def _create_dentist_user(self):
        user = CustomUser.objects.create_user(
            full_name="Test Dentist",
            email="d@test.com",
            role=UserTypeChoices.DENTIST,
            password="12branko34",
        )

        return user

    @patch.dict("Dudo_dent.accounts.signals.ROLE_PROFILE_HANDLERS", {
        UserTypeChoices.PATIENT: handle_patient_profile
    })
    def test_create_patient_profile_from_signal_expect_success(self):
        user = self._create_patient_user()

        handle_patient_profile(user)

        patient = Patient.objects.get(user=user)

        self.assertEqual(patient.email, user.email)


    @patch("Dudo_dent.accounts.signals.send_registration_conformation_email.delay")
    @patch.dict("Dudo_dent.accounts.signals.ROLE_PROFILE_HANDLERS", {
        UserTypeChoices.PATIENT: handle_patient_profile
    })
    def test_create_patient_send_conformation_email_expect_success(self, mock_send_email):
        user = self._create_patient_user()

        handle_patient_profile(user)
        mock_send_email(user.full_name, user.email)

        mock_send_email.assert_called_once_with("Patient One", "p@test.com")

    @patch('Dudo_dent.accounts.signals.GoogleCalendarManager')
    def test_creating_google_calendar_on_profile_creation_expect_success(self, mock_calendar_manager_class):
        mock_calendar_manager = MagicMock()
        mock_calendar_manager.create.return_value = "dentist test calendar"
        mock_calendar_manager_class.return_value = mock_calendar_manager

        user = self._create_dentist_user()
        handle_work_profile(user)

        create_google_calendar_for_dentist(sender=CustomUser, instance=user, created=True)

        profile = WorkProfile.objects.get(user=user)

        self.assertEqual(profile.google_calendar_id, "dentist test calendar")
        mock_calendar_manager.create.assert_called_once_with(user.full_name, user.pk)

