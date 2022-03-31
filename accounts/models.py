import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model based on AbstractBaseUser and CustomUserManager.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("Email"), max_length=255, unique=True)
    name = models.CharField(_("Name"), max_length=255)
    created_at = models.DateTimeField(_("Joined"), auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
    User Profile having one-to-one relation with CustomUser.
    """

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True
    )
    phone_regex = RegexValidator(
        regex=r"^\+(?:[0-9] ?){6,14}[0-9]$",
        message="Invalid Phone Number",
    )
    phone_no = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True)

    """Optional Fields"""
    org_name = models.CharField(_("Organization"), max_length=255, blank=True)
    address = models.TextField(_("Address"), blank=True)
    bank_name = models.CharField(_("Associated Bank Name"), max_length=512, blank=True)
    bank_acc = models.CharField(_("Bank Account No"), max_length=24, blank=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.user.email


class Feedback(models.Model):
    """
    User feedback
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser, verbose_name=_("User"), on_delete=models.CASCADE
    )
    subject = models.TextField(_("Subject"))
    description = models.TextField(_("Description"))

    class Meta:
        verbose_name = _("feedback")
        verbose_name_plural = _("feedbacks")

    def __str__(self):
        return self.user.email


class License(models.Model):

    """
    License model with 4 default Licensing option.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    LICENSE_CHOICES = (
        ("free", "Free"),
        ("trial", "Pro Trial"),
        ("pro", "Professional"),
        ("enterprise", "Enterprise"),
    )
    license_type = models.CharField(
        _("License Type"), max_length=15, choices=LICENSE_CHOICES, default="free"
    )
    name = models.CharField(_("License Name"), max_length=50, default="Free")
    price = models.PositiveIntegerField(_("License Price"), default=0)
    duration = models.DurationField(_("License Duration"), blank=True)

    class Meta:
        verbose_name = _("License")
        verbose_name_plural = _("Licenses")

    def __str__(self):
        return self.name


class UserLicense(models.Model):
    """
    UserLicense with one-to-one relation with CustomUser and License as foreign key.
    """

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True
    )
    assigned_license = models.ForeignKey(
        License,
        verbose_name=_("Assigned License"),
        related_name="licenses",
        on_delete=models.CASCADE,
    )
    current_license_qt = models.PositiveIntegerField(
        _("Current License Quantity"), default=1
    )
    current_license_price = models.PositiveIntegerField(
        _("Current License Price"), default=0
    )
    iat = models.DateTimeField(_("License Issued at"), auto_now=True)
    eat = models.DateTimeField(_("License Expires at"), auto_now_add=True)

    total_price = models.PositiveIntegerField(_("Total Price"), default=0)
    applied_for_pro = models.BooleanField(_("Applied For Pro"), default=False)

    LICENSE_CHOICES = (
        ("free", "Free"),
        ("trial", "Trial"),
        ("pro", "Professional"),
        ("enterprise", "Enterprise"),
    )
    applied_license = models.CharField(
        _("Applied for"), max_length=10, choices=LICENSE_CHOICES, blank=True
    )
    applied_license_qt = models.PositiveIntegerField(
        _("Applied License Quantity"), default=0
    )
    upgradingfrom_license = models.CharField(
        _("Upgrading from"), max_length=10, choices=LICENSE_CHOICES, blank=True
    )

    class Meta:
        verbose_name = _("User License")
        verbose_name_plural = _("User Licenses")

    def __str__(self):
        return self.user.email


class LoginEntry(models.Model):
    """
    User login entry from client Side. Admin Site logins will NOT get stored.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser, verbose_name=_("User"), on_delete=models.CASCADE
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


class PasswordReset(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        CustomUser,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
    )
    phone_no = models.CharField(_("Phone Number"), max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    otp_code = models.CharField(_("OTP Code"), max_length=6, blank=False)
    verified = models.BooleanField(_("Is Verified"), default=False)
    last_otp_time = models.DateTimeField(_("Last OTP time"), auto_now=True)

    class Meta:
        verbose_name = _("Password Reset")
        verbose_name_plural = _("Password Resets")

    def __str__(self):
        return self.user.email
