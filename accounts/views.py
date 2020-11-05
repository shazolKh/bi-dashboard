from datetime import datetime
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import (
    RetrieveAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings as jwt_settings

from dj_rest_auth.views import LogoutView

from .models import Profile, UserLicense
from .serializers import (
    RetrievePhoneSerializer,
    ProfileSerializer,
    LicenseUpdateSerializer,
)


class RetrievePhoneView(RetrieveAPIView):
    """
    Lookup user by phone number.
    """

    permission_classes = (AllowAny,)
    queryset = Profile.objects.all()
    serializer_class = RetrievePhoneSerializer

    def get_object(self):
        qs = self.get_queryset()
        return get_object_or_404(qs, phone_no=self.request.data["phone_no"])


class CustomLogoutView(LogoutView):
    """
    Update logout to be auth user only.
    """

    permission_classes = (IsAuthenticated,)


class CustomTokenRefreshView(TokenViewBase):
    """
    Send access token as http-only cookie when refreshing token.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        if getattr(settings, "REST_USE_JWT", False):
            cookie_name = getattr(settings, "JWT_AUTH_COOKIE", None)
            cookie_secure = getattr(settings, "JWT_AUTH_SECURE", False)
            cookie_httponly = getattr(settings, "JWT_AUTH_HTTPONLY", True)
            cookie_samesite = getattr(settings, "JWT_AUTH_SAMESITE", "Lax")
            if cookie_name:

                expiration = datetime.utcnow() + jwt_settings.ACCESS_TOKEN_LIFETIME
                response.set_cookie(
                    cookie_name,
                    serializer.validated_data["access"],
                    expires=expiration,
                    secure=cookie_secure,
                    httponly=cookie_httponly,
                    samesite=cookie_samesite,
                )
        return response


class ProfileView(RetrieveUpdateAPIView):
    """
    Read/Update User Profile.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    queryset = Profile.objects.all()

    def get_object(self):
        qs = self.get_queryset()
        return get_object_or_404(qs, user=self.request.user)


class LicenseUpdateView(UpdateAPIView):
    """
    Apply for Pro/Enterprise.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = LicenseUpdateSerializer

    queryset = UserLicense.objects.all()

    def get_object(self):
        qs = self.get_queryset()
        return get_object_or_404(qs, user=self.request.user)