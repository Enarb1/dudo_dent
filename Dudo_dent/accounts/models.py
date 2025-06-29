from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.accounts.managers import CustomUserManager
from Dudo_dent.patients.choices import PatientGenderChoices



# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        unique=True
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )


    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    @property
    def is_dentist(self):
        return self.groups.filter(name="dentist").exists()

    @property
    def is_patient(self):
        return hasattr(self, 'profile') and self.profile.profile_type == UserTypeChoices.PATIENT

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    full_name = models.CharField(
        max_length=150,
    )

    personal_id = models.CharField(
        max_length=50,
        unique=True,
    )

    age = models.IntegerField()

    profile_type = models.CharField(
        max_length=20,
        choices=UserTypeChoices,
        default=UserTypeChoices.PATIENT
    )

    phone_number = models.CharField(
        max_length=50,
    )

    gender = models.CharField(
        max_length=10,
        choices=PatientGenderChoices,
        default=PatientGenderChoices.OTHER,
    )

    patient = models.ForeignKey(
        to='patients.Patient',
        to_field='personal_id',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )


    def __str__(self):
        return self.full_name
