from django.contrib import admin

from Dudo_dent.patients.models import Patient


# Register your models here.

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'created_at',)
    list_filter = ('gender', 'age')


