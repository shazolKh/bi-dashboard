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


class License(models.Model):

    LICENSE_CHOICES = (
        ("free", "Free"),
        ("trial", "Trial"),
        ("pro", "Professional"),
        ("enterprise", "Enterprise"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(
        _("License Type"), max_length=10, choices=LICENSE_CHOICES, default="free"
    )
    name = models.CharField(_("License Name"), max_length=50, default="Free")
    price = models.PositiveIntegerField(_("License Price"), default=0)
    iat = models.DateTimeField(_("License Issued at"), auto_now_add=True)
    eat = models.DateTimeField(_("License Expires at"), null=True)

    class Meta:
        verbose_name = _("License")
        verbose_name_plural = _("Licenses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("license_detail", kwargs={"pk": self.pk})


class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    phone_regex = RegexValidator(
        regex=r"^\+(?:[0-9] ?){6,14}[0-9]$",
        message="Invalid Phone Number",
    )
    phone_no = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    """Optional Fields"""
    org_name = models.CharField(_("Organization"), max_length=255, blank=True)
    address = models.TextField(_("Address"), blank=True)
    bank_name = models.CharField(_("Associated Bank Name"), max_length=512, blank=True)
    bank_acc = models.CharField(_("Bank Account No"), max_length=24, blank=True)
    assigned_license = models.ForeignKey(
        License,
        verbose_name=_("Assigned License"),
        related_name="profiles",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.user.email


class LoginEntry(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(_("Login Timestamop"), auto_now_add=True)
    ip_address = models.GenericIPAddressField(
        _("Clients IP address"), protocol="both", unpack_ipv4=False
    )
    ip_address_type = models.CharField(_("Type of IP address"), max_length=50)
    user_agent = models.CharField(_("Clients User Agent"), max_length=255)

    class Meta:
        verbose_name = _("Login Entry")
        verbose_name_plural = _("Login Entries")

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse("loginentry_detail", kwargs={"pk": self.pk})