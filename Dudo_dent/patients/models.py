from django.contrib.auth import get_user_model
from django.db import models

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.accounts.models import CustomUser
from Dudo_dent.common.mixins.models_mixins import AgeCalculatorMixin
from Dudo_dent.patients.choices import PatientGenderChoices

# Create your models here.

UserModel = get_user_model()

class PatientBase(AgeCalculatorMixin, models.Model):
    class Meta:
        abstract = True
        ordering = ['full_name']

    full_name = models.CharField(
        max_length=150
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    email = models.EmailField(
        unique=True,
    )

    phone_number = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    personal_id = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=PatientGenderChoices,
        default=PatientGenderChoices.OTHER,
    )


    def __str__(self):
        return self.full_name


class Patient(PatientBase):
    user = models.OneToOneField(
        to=UserModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'role': UserTypeChoices.PATIENT},
        related_name='patient',
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
    )




    

    

