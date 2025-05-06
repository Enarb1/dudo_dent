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

    additional_info = models.TextField(
        blank=True,
        null=True
    )


    def get_procedures(self):
        return ', '.join(p.name for p in self.procedure.all())


    def __str__(self):
        formatted_date = self.date.strftime('%d.%m.%Y')
        return f"{formatted_date} - {self.patient.full_name} - {self.get_procedures()}"
