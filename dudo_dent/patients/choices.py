from django.db import models

class PatientGenderChoices(models.TextChoices):

    MALE = 'Мъж', 'Мъж'
    FEMALE = 'Жена', 'Жена'
    OTHER = 'Друг', 'Друг'