from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegistrationView, ProfileView

app_name = "accounts"

urlpatterns = [
    path("register/", RegistrationView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("refresh_token/", TokenRefreshView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)