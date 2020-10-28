from django.urls import path

from .views import (
    ProfileView,
    LicenseUpdateView,
)

app_name = "accounts"

urlpatterns = [
    path("user-profile/", ProfileView.as_view()),
    path("apply-for-license/", LicenseUpdateView.as_view()),
]
