from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


from Dudo_dent.accounts.constants import ROLE_PROFILE_HANDLERS
from Dudo_dent.accounts.tasks import send_registration_conformation_email
from Dudo_dent.appointments.google_calendar import GoogleCalendarManager
import logging

logger = logging.getLogger(__name__)

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    """
    When a new profile is created and uses a different handler
    and sends a conformation email to the user.
    """

    if not created:
        return

    handler = ROLE_PROFILE_HANDLERS.get(instance.role)

    if handler:
        handler(instance)
        send_registration_conformation_email.delay(instance.full_name, instance.email)


@receiver(post_save, sender=UserModel)
def create_google_calendar_for_dentist(sender, instance, created, **kwargs):
    """
    We make sure that the profile is created and that it is a dentist.
    Then we get the WorkProfile, so that we can add the Google Calendar ID
    """
    if not created or not instance.is_dentist:
        return

    try:
        profile = instance.get_profile()

        if profile and not profile.google_calendar_id:
            calendar_id = GoogleCalendarManager().create(instance.full_name, instance.pk)
            profile.google_calendar_id = calendar_id
            profile.save()
    except Exception as e:
        logger.exception(f"[Calendar ERROR] Could not create calendar for user {instance.pk}: {e}")


@receiver(pre_delete, sender=UserModel)
def delete_dentist_calendar(sender, instance, **kwargs):
    """Deleting the calendar connected to the dentist, when deleting his profile"""
    if instance.is_dentist:
        profile = instance.get_profile()
        if profile and profile.google_calendar_id:
            GoogleCalendarManager().delete(profile.google_calendar_id)

