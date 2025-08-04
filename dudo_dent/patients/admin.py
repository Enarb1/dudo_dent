from django.contrib import admin

from dudo_dent.patients.models import Patient


# Register your models here.

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    list_filter = ('gender', 'date_of_birth',)


