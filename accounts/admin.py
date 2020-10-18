from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
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
    # fields on user change form
    fieldsets = (
        ("Information", {"fields": ("name", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    # fields on user add form
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
    model = Profile

    list_display = (
        "get_email",
        "phone_no",
        "org_name",
        "bank_name",
        "bank_acc",
        "license_type",
        "license_iat",
        "license_duration",
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
                    "address",
                    "org_name",
                    "bank_name",
                    "bank_acc",
                )
            },
        ),
        (
            "Lincense Information",
            {
                "fields": (
                    "license_type",
                    "license_price",
                    "license_duration",
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
                    "address",
                    "org_name",
                    "bank_name",
                    "bank_acc",
                )
            },
        ),
        (
            "Lincense Information",
            {
                "fields": (
                    "license_type",
                    "license_price",
                    "license_duration",
                )
            },
        ),
    )

    search_fields = ("user__email",)

    ordering = [
        "-user__created_at",
    ]

    def get_email(self, instance):
        return instance.user.email

    get_email.short_description = "Email"