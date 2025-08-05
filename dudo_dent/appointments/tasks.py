from celery import shared_task

from dudo_dent.appointments.utils import send_mail_via_sendgrid


@shared_task
def send_appointment_conformation_mail(patient_name,patient_email, appointment_time, dentist_name):
    subject = f'Appointment Conformation for {dentist_name}'
    message = (f"Hi {patient_name},\n This a conformation for your appointment on "
               f"{appointment_time} with Dr.{dentist_name}.\n Greetings,\n Your Dudo Dent Team")

    send_mail_via_sendgrid(subject, message, patient_email)


@shared_task
def send_appointment_update(patient_name,patient_email, appointment_time, dentist_name):
    subject = f'Appointment Update'
    message = (f"Hi {patient_name},\n Your appointment was updated. Your new appointment is on "
               f"{appointment_time} with Dr.{dentist_name}.\n Greetings,\n Your Dudo Dent Team")

    send_mail_via_sendgrid(subject, message, patient_email)


@shared_task
def send_appointment_cancellation_email(patient_name,patient_email, appointment_time, dentist_name):
    subject = f'Appointment Cancellation'
    message = (f"Hi {patient_name},\n Your appointment for {appointment_time} with Dr.{dentist_name} "
               f"was cancelled. Please, contact us of you haven't requested the cancellation \n "
               f"Greetings,\n Your Dudo Dent Team")

    send_mail_via_sendgrid(subject, message, patient_email)

