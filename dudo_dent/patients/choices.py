from django.db import models

class PatientGenderChoices(models.TextChoices):

    MALE = 'Male', 'Мъж'
    FEMALE = 'Female', 'Жена'
    OTHER = 'Other', 'Друг'