from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime, timedelta

from django.urls import reverse

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

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(
        blank=True,
        null=True,
    )

    additional_info = models.TextField(
        blank=True,
        null=True,
    )

    google_event_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # def __str__(self):
    #     return f"{self.patient} - {self.start_time}"

    @property
    def datetime_display(self):
        return f"{self.date.strftime('%B %d, %Y')} at {self.start_time.strftime('%I:%M %p')}"


    def can_be_managed_by(self, user):
        return user.is_authenticated and (
                user.is_staff or
                user.is_superuser or
                user.is_dentist or
                user.is_nurse
        )

    def get_absolute_url(self):
        return reverse('appointment-details', kwargs={'pk': self.pk})

    """Making sure that the users have the correct role and avoiding mistakes by raw POST requests."""
    def clean(self):
        if self.dentist.role != UserTypeChoices.DENTIST:
            raise ValidationError("User is not a Dentist")

        if self.patient.role != UserTypeChoices.PATIENT:
            raise ValidationError("User is not a Patient")

    def save(self, *args, **kwargs):
        if self.start_time and not self.end_time:
            if self.date:
                full_start = datetime.combine(self.date, self.start_time)
                full_end = full_start + timedelta(minutes=15)
                self.end_time = full_end.time()
        super().save(*args, **kwargs)
