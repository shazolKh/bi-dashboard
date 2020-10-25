from django.contrib import admin
from django.urls import path, re_path, include
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("api/v1/", include("accounts.urls")),
    path("api/v1/account/", include("dj_rest_auth.urls")),
    path("api/v1/account/registration/", include("dj_rest_auth.registration.urls")),
    re_path(
        r"^api/v1/account/account-confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "api/v1/account/account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
]
