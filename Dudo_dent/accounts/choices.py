from django.db import models

class UserTypeChoices(models.TextChoices):
    DENTIST = 'dentist', "Dentist"
    PATIENT = 'patient', "Patient"
    NURSE = 'nurse', "Nurse"
    ADMIN = 'admin', "Admin"



