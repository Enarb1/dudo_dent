from django.db import models

class PatientGenderChoices(models.TextChoices):

    MALE = 'Male', 'Male'
    FEMALE = 'Female', 'Female'
    OTHER = 'Other', 'Other'