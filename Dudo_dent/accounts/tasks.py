from celery import shared_task
from django.core.mail import send_mail

from Dudo_dent import settings


@shared_task
def send_registration_conformation_email(user_full_name, user_email):
    subject = "Successful Registration"
    message = (f"Hi {user_full_name},\nYou have successfully registered for Dudo Dent.\n"
               f"Username: {user_email}\nThank you,\n"
               f"Your Dudo Dent Team")
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[user_email],
    )