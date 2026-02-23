import logging

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance: User, created: bool, **kwargs):
    """Automatically creates a Profile whenever a new User is created."""
    if created:
        Profile.objects.get_or_create(user=instance)
        logger.debug("Profile created for user: %s", instance.username)
