from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, LoginEntry, Profile, License


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
        ("Permission", {"fields": ("is_staff", "is_active")}),
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
        "get_license_eat",
    )

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
        (
            "License Information",
            {"fields": ("assigned_license",)},
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
        (
            "License Information",
            {"fields": ("assigned_license",)},
        ),
    )

    search_fields = (
        "user__email",
        "user__name",
    )

    ordering = [
        "-user__created_at",
    ]

    def get_name(self, instance):
        return instance.user.name

    get_name.short_description = "Name"

    def get_email(self, instance):
        return instance.user.email

    get_email.short_description = "Email"

    def get_license_name(self, instace):
        return instace.assigned_license.name

    get_license_name.short_description = "License"

    def get_license_eat(self, instace):
        return instace.assigned_license.eat

    get_license_eat.short_description = "License Expires"


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


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    model = License
    list_display = (
        "type",
        "name",
        "price",
        "iat",
        "eat",
    )

    list_filter = ("type",)
    search_fields = ("name",)

    ordering = [
        "-iat",
    ]
