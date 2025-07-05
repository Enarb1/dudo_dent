from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from Dudo_dent.accounts.constants import ROLE_PROFILE_HANDLERS



UserModel = get_user_model()

@receiver(post_save, sender=UserModel)

def create_profile(sender, instance, created, **kwargs):

    if not created:
        return

    handler = ROLE_PROFILE_HANDLERS.get(instance.role)

    if handler:
        handler(instance)

