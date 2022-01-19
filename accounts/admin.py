from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm, LicenseForm
from .models import CustomUser, Profile, License, UserLicense, LoginEntry, Feedback


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin config for User in AdminSite. Includes superuser, staff and regular user.
    """

    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = (
        "name",
        "email",
        "created_at",
        "is_staff",
        "is_active",
        "is_superuser",
    )
    list_filter = (
        "is_staff",
        "is_active",
    )
    """CustomUserChangeForm fields"""
    fieldsets = (
        ("Information", {"fields": ("name", "email", "password")}),
        ("Permissions", {
            "fields": (
                "is_staff",
                "is_active",
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
    )
    """CustomUserCreationForm fields"""
    add_fieldsets = (
        (
            "Information",
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = (
        "name",
        "email",
    )
    ordering = [
        "-created_at",
    ]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Profile Config for User Profile in AdminSite. Only shows users who have associated Profile.
    """

    model = Profile

    list_display = (
        "get_name",
        "get_email",
        "phone_no",
        "org_name",
        "address",
        "bank_name",
        "bank_acc",
        "get_license_name",
    )

    def get_name(self, instance):
        return instance.user.name

    get_name.short_description = "Name"

    def get_email(self, instance):
        return instance.user.email

    get_email.short_description = "Email"

    def get_license_name(self, instace):
        user_license = UserLicense.objects.get(user=instace.user)
        return user_license.assigned_license.name

    get_license_name.short_description = "License"

    fieldsets = (
        (
            "Identification",
            {
                "fields": (
                    "user",
                    "phone_no",
                )
            },
        ),
        (
            "General Information",
            {
                "fields": (
                    "org_name",
                    "address",
                    "bank_name",
                    "bank_acc",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            "Identification",
            {
                "fields": (
                    "user",
                    "phone_no",
                )
            },
        ),
        (
            "General Information",
            {
                "fields": (
                    "org_name",
                    "address",
                    "bank_name",
                    "bank_acc",
                )
            },
        ),
    )

    search_fields = (
        "user__email",
        "user__name",
        "bank_acc",
    )

    ordering = [
        "-user__created_at",
    ]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Feedback Config in Admin Site.
    """

    model = Feedback
    list_display = (
        "user",
        "subject",
        "description",
    )

    list_filter = ("user",)
    search_fields = ("user",)

    ordering = [
        "user",
    ]


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    """
    License Config in Admin Site. LicenseForm to show Duration widget.
    """

    model = License
    form = LicenseForm
    add_form = LicenseForm

    list_display = (
        "license_type",
        "name",
        "price",
        "duration",
    )

    list_filter = ("license_type",)
    search_fields = ("name",)

    ordering = [
        "name",
    ]


@admin.register(UserLicense)
class UserLicenseAdmin(admin.ModelAdmin):
    """
    UserLicense Config for Admin Site.
    """

    model = UserLicense

    list_display = (
        "get_email",
        "get_license_name",
        "get_license_price",
        "current_license_qt",
        "current_license_price",
        "iat",
        "eat",
        "total_price",
        "applied_license",
        "applied_license_qt",
        "applied_for_pro",
    )

    def save_model(self, request, obj, form, change):
        """
        Before saving UserLicense instance,
        1. If pro/enterprise and upgrading from pro/enterprise, expiry will start from current eat
        2. If pro/enterprise and upgrading from trial;, expiry will start from current time
        3. If free/trial, expiry will start from current time
        """

        current_license = License.objects.get(id=obj.assigned_license.id)

        cl_type = current_license.license_type
        cl_dur = current_license.duration
        cl_price = current_license.price
        upgrading_from = obj.upgradingfrom_license

        if cl_type == "pro" or cl_type == "enterprise":
            if upgrading_from == "trial":
                eat = timezone.now()
            else:
                eat = obj.eat
            obj.eat = eat + cl_dur * obj.current_license_qt
        else:
            obj.iat = timezone.now()
            obj.eat = timezone.now() + cl_dur

        obj.current_license_price = cl_price * obj.current_license_qt

        """Update total billing"""
        obj.total_price = obj.total_price + obj.current_license_price
        return obj.save()

    def get_email(self, instance):
        return instance.user.email

    get_email.short_description = "User Email"

    def get_license_name(self, instance):
        return instance.assigned_license.name

    get_license_name.short_description = "License Name"

    def get_license_price(self, instance):
        return instance.assigned_license.price

    get_license_price.short_description = "License Base Price"

    list_filter = (
        "assigned_license__license_type",
        "assigned_license__name",
    )
    search_fields = (
        "user__name",
        "user__email",
    )

    ordering = [
        "-iat",
    ]


@admin.register(LoginEntry)
class LoginEntryAdmin(admin.ModelAdmin):

    """
    Admin config to show login monitor table.
    """

    model = LoginEntry
    list_display = (
        "get_name",
        "get_email",
        "timestamp",
        "ip_address",
        "ip_address_type",
        "user_agent",
    )

    list_filter = ("ip_address_type",)

    search_fields = (
        "user__name",
        "user__email",
        "user_agent",
        "ip_address",
    )

    ordering = [
        "-timestamp",
    ]

    def get_name(self, instance):
        return instance.user.name

    get_name.short_description = "Name"

    def get_email(self, instance):
        return instance.user.email

    get_email.short_description = "Email"
