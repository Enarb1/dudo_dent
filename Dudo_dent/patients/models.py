from django.db import models
from django.utils.text import slugify

from Dudo_dent.patients.choices import PatientGenderChoices

# Create your models here.

class Patient(models.Model):
    full_name = models.CharField(
        max_length=150
    )

    age = models.IntegerField()

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        max_length=30,
    )

    personal_id = models.CharField(
        max_length=30,
    )

    gender = models.CharField(
        max_length=10,
        choices=PatientGenderChoices,
        default=PatientGenderChoices.OTHER,
    )
    
    slug = models.SlugField(
        blank=True,
        unique=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    
    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if not self.slug:
            self.slug = slugify(f"{self.id}-{self.full_name}")
            
        super().save(*args, **kwargs)
