from django.contrib import admin
from django.urls import path, include, re_path
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView
from django.views.generic import TemplateView

from django.contrib.auth.views import (
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("accounts.urls")),
    path(
        "api/v1/account-confirm-email/<str:key>/",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "api/v1/account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    path(
        "api/v1/password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "api/v1/password/reset/complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
