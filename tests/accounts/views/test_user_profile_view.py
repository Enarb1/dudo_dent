from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from dudo_dent.patients.choices import PatientGenderChoices

UserModel = get_user_model()

class TestUserRegisterView(TestCase):
    def setUp(self):
        self.user_credentials = {
            'full_name': 'Test User',
            'email': 'user_reg_test@test.com',
            'password1': '12branko34',
            'password2': '12branko34',
            'gender': PatientGenderChoices.OTHER,
        }

    def test_user_redirection_after_registration(self):
        register_url = reverse('register')
        home_url = reverse('home')

        response = self.client.post(register_url, data=self.user_credentials)

        self.assertRedirects(response, home_url)

    def test_user_if_logged_in_after_registration(self):

        self.client.post(reverse('register'), data=self.user_credentials)

        user = UserModel.objects.get(email=self.user_credentials['email'])

        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

    