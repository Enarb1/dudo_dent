from django.db import models

from Dudo_dent.accounts.models import CustomUser
from Dudo_dent.patients.choices import PatientGenderChoices

# Create your models here.

class Patient(models.Model):
    full_name = models.CharField(
        max_length=150
    )

    age = models.IntegerField()

    email = models.EmailField(
        blank=True,
        null=True,
        unique=True,
    )

    phone_number = models.CharField(
        max_length=30,
    )

    personal_id = models.CharField(
        max_length=30,
        unique=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=PatientGenderChoices,
        default=PatientGenderChoices.OTHER,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    dentist = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='patients',
    )
    
    def __str__(self):
        return self.full_name
    

