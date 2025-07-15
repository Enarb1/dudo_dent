from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.patients.models import Patient


# Create your models here.

UserModel = get_user_model()
class Appointment(models.Model):
    class Meta:
        unique_together = ('dentist', 'start_time')


    patient = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='patient_appointments',
    )

    dentist = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='dentist_appointments',
        limit_choices_to={'role': UserTypeChoices.DENTIST},
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    google_event_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.patient} - {self.start_time} with {self.dentist}"

    """Making sure that the users have the correct role and avoiding mistakes by raw POST requests."""
    def clean(self):
        if self.dentist.role != UserTypeChoices.DENTIST:
            raise ValidationError("User is not a Dentist")

        if self.patient.role != UserTypeChoices.PATIENT:
            raise ValidationError("User is not a Patient")
