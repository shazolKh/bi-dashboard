from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    ProfileView,
    LicenseUpdateView,
)

app_name = "accounts"

urlpatterns = [
    path("user-profile/", ProfileView.as_view()),
    path("apply-for-license/", LicenseUpdateView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)