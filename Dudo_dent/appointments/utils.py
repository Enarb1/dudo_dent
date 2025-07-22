from datetime import date

from Dudo_dent.appointments.models import Appointment


def get_appointments_for_today(user):
    today = date.today()

    if not user.is_authenticated:
        return Appointment.objects.none()

    if user.is_patient:
        return Appointment.objects.filter(patient_id=user.id, date__gte=today).order_by('date')
    if user.is_dentist:
        return Appointment.objects.filter(dentist_id=user.id, date=today).order_by('date')

    return Appointment.objects.filter(date=today)
