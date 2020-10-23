from django.utils import timezone
from django.dispatch import Signal
from django.contrib.auth.models import Group, Permission

from ipware import get_client_ip

from .models import CustomUser, LoginEntry, Profile, License, UserLicense


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


def change_user_profile(sender, instance, created, **kwargs):
    """
    Automatically generates and updates a profile when an User is created on post_save signal.
    """
    is_admin = instance.is_staff or instance.is_superuser

    if not is_admin:
        if created:
            if hasattr(instance, "phone_no"):
                phone_no = instance.phone_no
                delattr(instance, "phone_no")
            else:
                phone_no = ""
            Profile.objects.create(user=instance, phone_no=phone_no)

            """Assign a default free license to User"""
            default_license = License.objects.get(license_type="free")
            UserLicense.objects.create(user=instance, assigned_license=default_license)
        else:
            instance.profile.save()


"""Custom Signal dispatcher to trigger when user logs in"""
login_signal = Signal(providing_args=["request", "user_email"])


def store_login_information(sender, request, user_email, **kwargs):
    """
    Create login entry with ip and user_agent everytime user logs in.
    """
    user = sender.objects.get(email=user_email)
    is_admin = user.is_staff or user.is_superuser

    if not is_admin:
        client_ip, is_routable = get_client_ip(request)
        if is_routable:
            ip_address_type = "Public"
        else:
            ip_address_type = "Private"

        if client_ip is None:
            raise ValueError("IP not found.")
        else:
            LoginEntry.objects.create(
                user=user,
                timestamp=timezone.now(),
                ip_address=client_ip,
                ip_address_type=ip_address_type,
                user_agent=request.META["HTTP_USER_AGENT"],
            )
