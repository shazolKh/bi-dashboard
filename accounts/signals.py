from django.contrib.auth.models import Group, Permission

from .models import CustomUser, Profile


def create_staff_group(sender, **kwargs):
    """
    Create Staff group after migrate command on post_migrate signal.
    """
    permissions = [
        Permission.objects.get(codename="add_profile"),
        Permission.objects.get(codename="change_profile"),
        Permission.objects.get(codename="view_profile"),
        Permission.objects.get(codename="delete_profile"),
    ]
    group = Group.objects.create(name="Staff")
    [group.permissions.add(permission) for permission in permissions]


def add_admin_permission(sender, instance, created, **kwargs):
    """
    Add user with is_staff to Staff group on post_save signal.
    """
    if created and instance.is_staff:
        staff_group = Group.objects.get(name="Staff")
        staff_group.user_set.add(instance)


def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically generates a profile when an User is created on post_save signal.
    """
    is_admin = instance.is_staff or instance.is_superuser
    if created and not is_admin:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    """
    Automatically updates a profile when any User field is updated on post_save signal.
    """
    is_admin = instance.is_staff or instance.is_superuser
    if not is_admin:
        instance.profile.save()