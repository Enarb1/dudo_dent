from django.contrib import admin

from Dudo_dent.appointments.models import Appointment


# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'start_time', 'dentist', 'created_at')
    readonly_fields = ('created_at','google_event_id')

