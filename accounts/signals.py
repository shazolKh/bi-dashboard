from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import CustomUser, Profile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically generates a profile when an User is created.
    """
    is_admin = instance.is_staff or instance.is_superuser
    if created and not is_admin:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """
    Automatically updates a profile when any User field is updated.
    """
    is_admin = instance.is_staff or instance.is_superuser
    if not is_admin:
        instance.profile.save()