import uuid
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model based on AbstractBaseUser and CustomUserManager.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("Email Address"), max_length=255, unique=True)
    name = models.CharField(_("Name"), max_length=255)
    created_at = models.DateTimeField(_("Joined at"), auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("Custom User")
        verbose_name_plural = _("Custom Users")

    def __str__(self):
        return self.email


class Profile(models.Model):

    # mandatory fields
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'.\nAt most 15 digits are allowed.",
    )
    phone_no = models.CharField(validators=[phone_regex], max_length=17)

    # optional fields
    org_name = models.CharField(_("Organization"), max_length=255, blank=True)
    address = models.TextField(_("Address"), blank=True)
    bank_name = models.CharField(_("Associated Bank Name"), max_length=512, blank=True)
    bank_acc = models.CharField(_("Bank Account No"), max_length=24, blank=True)

    # license fields
    LICENSE_CHOICES = (
        ("free", "Free"),
        ("trial", "Trial"),
        ("pro", "Pro"),
    )
    license_type = models.CharField(
        _("License Type"), max_length=10, choices=LICENSE_CHOICES, default="free"
    )
    license_price = models.PositiveIntegerField(_("License Price"), default=0)
    license_iat = models.DateTimeField(_("License Issued at"), auto_now_add=True)
    license_duration = models.DurationField(_("License Duration"), null=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.user.email
