from django.db import models

from Dudo_dent.procedures.models import Procedure
from Dudo_dent.patients.models import Patient

# Create your models here.

class Visit(models.Model):
    date = models.DateField()
    patient = models.ForeignKey(
        to=Patient,
        on_delete=models.CASCADE,
        related_name='visits',
    )

    procedure = models.ManyToManyField(
        Procedure,
        related_name='visits',
    )

    def __str__(self):
        return f"{self.date}-{self.patient.full_name}"
