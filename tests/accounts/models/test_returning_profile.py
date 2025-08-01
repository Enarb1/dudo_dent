import datetime
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.test import TestCase

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.accounts.models import CustomUser, WorkProfile
from Dudo_dent.accounts.services.user_profile_services import handle_work_profile, handle_patient_profile
from Dudo_dent.accounts.signals import create_profile
from Dudo_dent.patients.choices import PatientGenderChoices
from Dudo_dent.patients.models import Patient

UserModel = get_user_model()


class TestReturningProfile(TestCase):

    def setUp(self):
        post_save.disconnect(create_profile, sender=CustomUser)
        self.addCleanup(post_save.connect, create_profile, sender=CustomUser)


    def _create_test_user(self, role, email):
        return CustomUser.objects.create_user(
            email=email,
            full_name=f'{role} Test',
            role=role,
            password='12branko34',
        )


    @patch('Dudo_dent.accounts.signals.GoogleCalendarManager.create')
    def test_get_dentist_profile_expect_success(self, mock_calendar_create):
        mock_calendar_create.return_value = 'mock calendar_id'

        user = self._create_test_user(UserTypeChoices.DENTIST, 'd.test@abv.bg')

        handle_work_profile(user)

        self.assertTrue(user.is_dentist)
        self.assertIsInstance(user.get_profile(), WorkProfile,)


    @patch('Dudo_dent.accounts.signals.GoogleCalendarManager.create')
    def test_get_nurse_profile_expect_success(self, mock_calendar_create):
        mock_calendar_create.return_value = 'mock calendar_id'

        user = self._create_test_user(UserTypeChoices.NURSE, 'n.test@abv.bg')
        handle_work_profile(user)

        self.assertIsInstance(user.get_profile(), WorkProfile)
        self.assertTrue(user.is_nurse)



    @patch('Dudo_dent.accounts.signals.send_registration_conformation_email.delay')
    def test_patient_custom_user_and_patient_user_connection_expect_success(self, mock_send_mail):
        mock_send_mail.return_value = 'mock_email'

        existing_patient = Patient.objects.create(
            full_name='Patient One',
            email="p@test.com",
            personal_id='PATIENT123',
            gender=PatientGenderChoices.OTHER,
        )
        existing_patient.save()

        user = self._create_test_user(UserTypeChoices.PATIENT, 'p@test.com')

        handle_patient_profile(user)

        existing_patient.refresh_from_db()
        self.assertEqual(existing_patient.user, user)



