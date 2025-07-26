from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime, timedelta

from django.urls import reverse

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.appointments.choices import WeekdayChoices
from Dudo_dent.patients.models import Patient


# Create your models here.

UserModel = get_user_model()
class Appointment(models.Model):
    class Meta:
        unique_together = ('dentist', 'date', 'start_time')


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

    def save(self, *args, **kwargs):
        if self.date and self.start_time:
            full_start = datetime.combine(self.date, self.start_time)
            full_end = full_start + timedelta(minutes=15)
            self.end_time = full_end.time()
        super().save(*args, **kwargs)


class AvailabilityRule(models.Model):
   dentist = models.ForeignKey(
       to=UserModel,
       on_delete=models.CASCADE,
       related_name='availability',
       limit_choices_to={'role': UserTypeChoices.DENTIST},
   )

   weekdays = ArrayField(models.CharField(
       max_length=3,
       choices=WeekdayChoices,
   ))

   start_time = models.TimeField()
   end_time = models.TimeField()

   valid_from = models.DateField()
   valid_to = models.DateField()

   def get_weekday_labels(self):
       return [WeekdayChoices(value).label for value in self.weekdays]


class UnavailabilityRule(models.Model):
   dentist = models.ForeignKey(
       to=UserModel,
       on_delete=models.CASCADE,
       related_name='unavailability',
   )

   start_date = models.DateField()
   end_date = models.DateField()

   reason = models.TextField(
       max_length=255,
       blank=True,
       null=True,
   )
