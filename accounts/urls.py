from django.conf import settings
from django.urls import path, include

from dj_rest_auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetView,
    UserDetailsView,
)
from dj_rest_auth.registration.views import RegisterView

from .views import (
    ProfileView,
    LicenseUpdateView,
    CustomTokenRefreshView,
)

app_name = "accounts"

urlpatterns = [
    # URLs that do not require a session or valid token
    path("registration/", RegisterView.as_view(), name="rest_register"),
    path("login/", LoginView.as_view(), name="rest_login"),
    path(
        "password/reset/",
        PasswordResetView.as_view(),
        name="rest_password_reset",
    ),
    # URLs that require a user to be logged in with a valid session / token.
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("user/profile/", ProfileView.as_view()),
    path("user/dashboard/", include("powerbi.urls")),
    path("user/apply-for-license/", LicenseUpdateView.as_view()),
    path(
        "password/change/",
        PasswordChangeView.as_view(),
        name="rest_password_change",
    ),
]

if getattr(settings, "REST_USE_JWT", False):
    from rest_framework_simplejwt.views import TokenVerifyView

    urlpatterns += [
        path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
        path(
            "token/refresh/",
            CustomTokenRefreshView.as_view(),
            name="token_refresh",
        ),
    ]
