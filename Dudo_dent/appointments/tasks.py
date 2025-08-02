from celery import shared_task
from django.core.mail import send_mail

from Dudo_dent import settings

import logging
logger = logging.getLogger(__name__)

@shared_task
def send_appointment_conformation_mail(patient_name,patient_email, appointment_time, dentist_name):
    subject = f'Appointment Conformation for {dentist_name}'
    message = (f"Hi {patient_name},\n This a conformation for your appointment on "
               f"{appointment_time} with Dr.{dentist_name}.\n Greetings,\n Your Dudo Dent Team")
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(subject, message, from_email, [patient_email])
        logger.info(f"Sent confirmation email to {patient_email}")
    except Exception as e:
        logger.error(f"Failed to send confirmation email to {patient_email}: {str(e)}", exc_info=True)


@shared_task
def send_appointment_update(patient_name,patient_email, appointment_time, dentist_name):
    subject = f'Appointment Update'
    message = (f"Hi {patient_name},\n Your appointment was updated. Your new appointment is on "
               f"{appointment_time} with Dr.{dentist_name}.\n Greetings,\n Your Dudo Dent Team")
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(subject, message, from_email, [patient_email])
        logger.info(f"Sent appointment update email to {patient_email}")
    except Exception as e:
        logger.error(f"Failed to send appointment update email to {patient_email}: {str(e)}", exc_info=True)


@shared_task
def send_appointment_cancellation_email(patient_name,patient_email, appointment_time, dentist_name):
    subject = f'Appointment Cancellation'
    message = (f"Hi {patient_name},\n Your appointment for {appointment_time} with Dr.{dentist_name} "
               f"was cancelled. Please, contact us of you haven't requested the cancellation \n "
               f"Greetings,\n Your Dudo Dent Team")
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(subject, message, from_email, [patient_email])
        logger.info(f"Sent cancellation email to {patient_email}")
    except Exception as e:
        logger.error(f"Failed to send cancellation email to {patient_email}: {str(e)}", exc_info=True)
