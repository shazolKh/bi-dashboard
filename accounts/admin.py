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
    )
    list_filter = (
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("name", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
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
        "get_name",
        "get_email",
        "phone_no",
        "org_name",
        "bank_name",
        "bank_acc",
    )

    search_fields = (
        "user__name",
        "user__email",
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