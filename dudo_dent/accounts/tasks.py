from celery import shared_task

from dudo_dent.appointments.utils import send_mail_via_sendgrid


@shared_task
def send_registration_conformation_email(user_full_name, user_email):
    subject = "Successful Registration"
    message = (f"Hi {user_full_name},\nYou have successfully registered for Dudo Dent.\n"
               f"Username: {user_email}\nThank you,\n"
               f"Your Dudo Dent Team")

    send_mail_via_sendgrid(subject, message, user_email)
