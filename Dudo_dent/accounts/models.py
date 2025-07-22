from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.accounts.managers import CustomUserManager
from Dudo_dent.common.mixins.models_mixins import AgeCalculatorMixin


# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):

    full_name = models.CharField(
        max_length=200,
    )

    email = models.EmailField(
        unique=True
    )

    role = models.CharField(choices=UserTypeChoices)

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name
    @property
    def is_dentist(self):
        return self.role == UserTypeChoices.DENTIST

    @property
    def is_patient(self):
        return self.role == UserTypeChoices.PATIENT

    @property
    def is_nurse(self):
        return self.role == UserTypeChoices.NURSE

    @property
    def is_admin(self):
        return self.role == UserTypeChoices.ADMIN

    def get_profile(self):
        if self.is_nurse or self.is_dentist:
            return getattr(self, "workprofile", None)
        if self.is_patient:
            return getattr(self, "patient", None)

        return None



class WorkProfile(AgeCalculatorMixin, models.Model):
    user = models.OneToOneField(
        to=CustomUser,
        on_delete=models.CASCADE,
    )

    phone_number = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    address = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    google_calender_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )


