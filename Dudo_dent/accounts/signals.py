from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


from Dudo_dent.accounts.constants import ROLE_PROFILE_HANDLERS
from Dudo_dent.appointments.google_calender import create_calendar

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)

def create_profile(sender, instance, created, **kwargs):

    if not created:
        return

    handler = ROLE_PROFILE_HANDLERS.get(instance.role)

    if handler:
        handler(instance)


@receiver(post_save, sender=UserModel)
def create_google_calendar_for_dentist(sender, instance, created, **kwargs):
    """
    We make sure that the profile is created and that it is a dentist.
    Then we get the WorkProfile, so that we can add the Google Calendar ID
    """
    if not created or not instance.is_dentist:
        return

    profile = instance.get_profile()

    if profile and not profile.google_calender_id:
        calendar_id = create_calendar(instance.full_name, instance.pk)
        profile.google_calender_id = calendar_id
        profile.save()
