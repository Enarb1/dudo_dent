from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from Dudo_dent.appointments.models import Appointment
from Dudo_dent.appointments.tasks import send_appointment_conformation_mail, send_appointment_update, \
    send_appointment_cancellation_email


@receiver(post_save, sender=Appointment)
def send_conformation_on_booking(sender, instance, created, **kwargs):
    patient = instance.patient
    dentist = instance.dentist

    appointment_time = f"{instance.date} at {instance.start_time}"
    if not patient.email:
        return

    if created:
        send_appointment_conformation_mail.delay(
            patient.full_name,
            patient.email,
            appointment_time,
            dentist.full_name,
        )
    else:
        send_appointment_update.delay(
            patient.full_name,
            patient.email,
            appointment_time,
            dentist.full_name,
        )


@receiver(pre_delete, sender=Appointment)
def send_cancellation_conformation(sender, instance, **kwargs):
    patient = instance.patient
    dentist = instance.dentist

    if not patient.email:
        return

    appointment_time = f"{instance.date} at {instance.start_time}"

    send_appointment_cancellation_email.delay(
        patient.full_name,
        patient.email,
        appointment_time,
        dentist.full_name,
    )
